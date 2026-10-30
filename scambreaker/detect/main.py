from fastapi import FastAPI
from pydantic import BaseModel

# Detection and memory modules
from detect.rules import detect_rules
from detect.memory import ConversationMemory
from detect.groq_client import analyze_with_groq


app = FastAPI(
    title="ScamBreaker Detection API",
    description="AI-powered scam conversation analysis",
    version="1.0"
)


# ---------------------------------------------------------
# Conversation memory
# ---------------------------------------------------------

memory = ConversationMemory()


# ---------------------------------------------------------
# Request Models
# ---------------------------------------------------------

class AnalyzeRequest(BaseModel):
    text: str
    ts: float
    call_id: str


class ResetRequest(BaseModel):
    call_id: str


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "ScamBreaker Detection Backend"
    }


# ---------------------------------------------------------
# Main Scam Analysis Endpoint
# ---------------------------------------------------------

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    text = request.text.strip()
    lower_text = text.lower()

    # -----------------------------------------------------
    # Analyze current message using rule-based detection
    # -----------------------------------------------------

    message_score, message_reasons = detect_rules(text)

    # -----------------------------------------------------
    # Analyze current message using Groq
    #
    # Groq is optional. If unavailable, the rule-based
    # detector continues working normally.
    # -----------------------------------------------------

    groq_analysis = analyze_with_groq(text)

    # -----------------------------------------------------
    # Determine stage for current message
    #
    # Stage 1 = Hook
    # Stage 2 = Fake Authority
    # Stage 3 = Threat / Isolation
    # Stage 4 = Financial Exploitation
    # -----------------------------------------------------

    if any("Financial" in reason for reason in message_reasons):
        current_stage = 4

    elif (
        any("Threat" in reason for reason in message_reasons)
        or any("Isolation" in reason for reason in message_reasons)
    ):
        current_stage = 3

    elif any("Authority" in reason for reason in message_reasons):
        current_stage = 2

    else:
        current_stage = 0

    # -----------------------------------------------------
    # Update cumulative conversation memory
    # -----------------------------------------------------

    call = memory.update(
        request.call_id,
        text,
        message_score,
        message_reasons,
        current_stage
    )

    cumulative_score = call["score"]
    reasons = call["reasons"]
    stage = call["stage"]

    # -----------------------------------------------------
    # Determine Risk Level
    # -----------------------------------------------------

    if cumulative_score > 65:
        level = "red"

    elif cumulative_score >= 30:
        level = "yellow"

    else:
        level = "green"

    # -----------------------------------------------------
    # Identify caller's claimed identity
    #
    # IMPORTANT:
    # ConversationMemory stores messages as strings.
    # Therefore we search the complete conversation text.
    # -----------------------------------------------------

    claim = "Unknown"
    scam_type = "unknown"

    conversation_text = " ".join(
        message.lower()
        for message in call["messages"]
    )

    if "cbi" in conversation_text:
        claim = "CBI officer"
        scam_type = "cbi"

    elif "police" in conversation_text:
        claim = "Police officer"
        scam_type = "police"

    elif "rbi" in conversation_text:
        claim = "RBI representative"
        scam_type = "bank"

    elif (
        "calling from your bank" in conversation_text
        or "bank official" in conversation_text
    ):
        claim = "Bank representative"
        scam_type = "bank"

    # -----------------------------------------------------
    # Verification limitation
    #
    # False means supporting proof was not detected.
    # It does NOT mean the identity was verified as false.
    # -----------------------------------------------------

    proof = False

    # -----------------------------------------------------
    # Predict scammer's likely next move
    # -----------------------------------------------------

    if any("Financial" in reason for reason in reasons):

        next_move = (
            "The caller may next demand money, an OTP, UPI PIN, "
            "bank password, or another payment-related action. "
            "Do not transfer money or share financial credentials."
        )

    elif any("Isolation" in reason for reason in reasons):

        next_move = (
            "The caller may next try to prevent you from contacting "
            "family, your bank, or the authorities. Do not stay isolated. "
            "End the interaction and verify independently."
        )

    elif any("Threat" in reason for reason in reasons):

        next_move = (
            "The caller may next increase pressure by threatening arrest, "
            "legal action, or account consequences. Do not act under pressure. "
            "Verify the claim independently."
        )

    elif any("Authority" in reason for reason in reasons):

        next_move = (
            "The caller may next introduce a fake investigation, legal case, "
            "or urgent verification request. Do not share personal or financial "
            "information. Verify the caller independently."
        )

    elif level == "yellow":

        next_move = (
            "Be cautious. Do not share OTPs, PINs or passwords. "
            "Verify the caller independently."
        )

    else:

        next_move = (
            "No strong scam indicators detected so far. "
            "Continue to stay cautious."
        )

    # -----------------------------------------------------
    # API Response
    # -----------------------------------------------------

    return {

        # Eight core fields
        "level": level,
        "score": cumulative_score,
        "scam_type": scam_type,
        "stage": stage,
        "claim": claim,
        "proof": proof,
        "reasons": reasons,
        "next_move": next_move,

        # Optional Groq explanation
        "ai_analysis": groq_analysis,

        # Testing / integration metadata
        "call_id": request.call_id,
        "message_score": message_score,
        "messages_analyzed": len(call["messages"])
    }


# ---------------------------------------------------------
# Reset a Conversation
# ---------------------------------------------------------

@app.post("/reset")
def reset_conversation(request: ResetRequest):

    return memory.reset(request.call_id)


# ---------------------------------------------------------
# Root Endpoint
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "ScamBreaker Detection API is running",
        "docs": "/docs"
    }