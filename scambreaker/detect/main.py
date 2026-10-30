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


# Request models
class AnalyzeRequest(BaseModel):
    text: str
    ts: float
    call_id: str


class ResetRequest(BaseModel):
    call_id: str


# Health check
@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "ScamBreaker Detection Backend"
    }


# Main scam analysis endpoint
@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    text = request.text.strip()
    lower_text = text.lower()

    # Analyze the current message
    message_score, message_reasons = detect_rules(text)

    # Determine the stage indicated by this message
    if any("Financial" in reason for reason in message_reasons):
        current_stage = 4

    elif any("Isolation" in reason for reason in message_reasons):
        current_stage = 3

    elif any("Threat" in reason for reason in message_reasons):
        current_stage = 2

    elif any("Authority" in reason for reason in message_reasons):
        current_stage = 1

    else:
        current_stage = 0

    # Update cumulative conversation memory
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

    # Determine risk level
    if cumulative_score > 65:
        level = "red"

    elif cumulative_score >= 30:
        level = "yellow"

    else:
        level = "green"

    # Identify the caller's claimed identity.
    # This is only a claim, not verified identity.
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

    # Explain the verification limitation
    proof = False

    # Suggest a safe next action
    if level == "red":
        next_move = (
            "Stop sharing information or transferring money. "
            "End the interaction and independently contact the "
            "official organization."
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

    # API response
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


# Reset a conversation
@app.post("/reset")
def reset_conversation(request: ResetRequest):

    return memory.reset(request.call_id)


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "ScamBreaker Detection API is running",
        "docs": "/docs"
    }