from fastapi import FastAPI
from pydantic import BaseModel

# Correct imports when running from the project root
from detect.rules import detect_rules
from detect.memory import ConversationMemory


app = FastAPI(
    title="ScamBreaker Detection API",
    description="AI-powered scam conversation analysis",
    version="1.0"
)


# Conversation memory
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
    # Analyze the current message
    # -----------------------------------------------------

    message_score, message_reasons = detect_rules(text)


    # -----------------------------------------------------
    # Determine the stage indicated by this message
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
    # Identify the caller's claimed identity
    #
    # This is only a claim, not verified identity.
    # -----------------------------------------------------

    claim = "Unknown"
    scam_type = "unknown"


    if "cbi" in lower_text:
        claim = "CBI officer"
        scam_type = "cbi"

    elif "police" in lower_text:
        claim = "Police officer"
        scam_type = "police"

    elif "rbi" in lower_text:
        claim = "RBI representative"
        scam_type = "bank"

    elif (
        "calling from your bank" in lower_text
        or "bank official" in lower_text
    ):
        claim = "Bank representative"
        scam_type = "bank"


    # -----------------------------------------------------
    # Explain the verification limitation
    #
    # False means supporting proof was not detected.
    # It does NOT mean the identity was verified as false.
    # -----------------------------------------------------

    proof = False


    # -----------------------------------------------------
    # Predict the scammer's likely next move
    #
    # Prediction is based on the manipulation techniques
    # detected in the conversation.
    # -----------------------------------------------------

       # -----------------------------------------------------
    # Predict the scammer's likely next move
    #
    # Prediction is based on the manipulation techniques
    # detected in the conversation.
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

        # Eight core fields for the frontend
        "level": level,
        "score": cumulative_score,
        "scam_type": scam_type,
        "stage": stage,
        "claim": claim,
        "proof": proof,
        "reasons": reasons,
        "next_move": next_move,

        # Additional testing metadata
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