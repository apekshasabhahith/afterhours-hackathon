from fastapi import FastAPI
from pydantic import BaseModel
from rules import detect_rules
from memory import ConversationMemory

# ==========================================
# 1. INITIALIZE APPLICATION
# ==========================================

app = FastAPI(
    title="ScamBreaker Detection API",
    description="AI-powered scam conversation analysis",
    version="1.0"
)

# Initialize conversation memory
memory = ConversationMemory()


# ==========================================
# 2. REQUEST MODEL
# ==========================================

class AnalyzeRequest(BaseModel):
    text: str
    ts: float
    call_id: str


class ResetRequest(BaseModel):
    call_id: str


# ==========================================
# 3. HEALTH CHECK
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "running",
        "service": "ScamBreaker Detection Backend"
    }


# ==========================================
# 4. SCAM ANALYSIS
# ==========================================

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    text = request.text.strip()
    lower_text = text.lower()

    # Run detection rules
    score, reasons = detect_rules(text)

    # ======================================
    # MANIPULATION STAGE CLASSIFICATION
    # ======================================

    if any("Financial" in r for r in reasons):
        stage = 4

    elif any("Isolation" in r for r in reasons):
        stage = 3

    elif any("Threat" in r for r in reasons):
        stage = 2

    elif any("Authority" in r for r in reasons):
        stage = 1

    else:
        stage = 0

    # ======================================
    # UPDATE CONVERSATION MEMORY
    # ======================================

    call = memory.update(
        request.call_id,
        text,
        score,
        reasons,
        stage
    )

    # Use cumulative conversation score
    cumulative_score = call["score"]

    # ======================================
    # RISK CLASSIFICATION
    # ======================================

    if cumulative_score >= 65:
        level = "red"

    elif cumulative_score >= 30:
        level = "yellow"

    else:
        level = "green"

    # ======================================
    # CALLER IDENTITY CLASSIFICATION
    # ======================================

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

    # ======================================
    # NEXT-MOVE PREDICTION
    # ======================================

    if call["stage"] == 4:
        next_move = (
            "May attempt further financial exploitation "
            "or request banking credentials"
        )

    elif call["stage"] == 3:
        next_move = (
            "May increase pressure to keep "
            "the conversation secret"
        )

    elif call["stage"] == 2:
        next_move = (
            "May escalate threats or intimidation"
        )

    elif call["stage"] == 1:
        next_move = (
            "May attempt to establish false authority"
        )

    else:
        next_move = (
            "No suspicious next move identified"
        )

    # ======================================
    # FINAL RESPONSE
    # ======================================

    return {
        "call_id": request.call_id,
        "level": level,
        "score": cumulative_score,
        "message_score": score,
        "scam_type": scam_type,
        "stage": call["stage"],
        "claim": claim,
        "proof": False,
        "reasons": call["reasons"],
        "next_move": next_move,
        "messages_analyzed": len(call["messages"])
    }


# ==========================================
# 5. RESET CONVERSATION
# ==========================================

@app.post("/reset")
def reset_conversation(request: ResetRequest):

    return memory.reset(request.call_id)


# ==========================================
# 6. ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "ScamBreaker P2 Detection API is running"
    }