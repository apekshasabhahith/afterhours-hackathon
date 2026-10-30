from fastapi import FastAPI
from pydantic import BaseModel
from rules import detect_rules

app = FastAPI(
    title="ScamBreaker Detection API",
    description="AI-powered scam conversation analysis",
    version="1.0"
)


# ==========================================
# 1. REQUEST MODEL
# ==========================================

class AnalyzeRequest(BaseModel):
    text: str
    ts: float
    call_id: str


# ==========================================
# 2. HEALTH CHECK
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "running",
        "service": "ScamBreaker Detection Backend"
    }


# ==========================================
# 3. SCAM ANALYSIS
# ==========================================

@app.post("/analyze")
def analyze(request: AnalyzeRequest):

    text = request.text.strip()
    lower_text = text.lower()

    # Run detection rules
    score, reasons = detect_rules(text)

    # ======================================
    # RISK CLASSIFICATION
    # ======================================

    if score > 65:
        level = "red"

    elif score >= 30:
        level = "yellow"

    else:
        level = "green"

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

    if stage == 4:

        next_move = (
            "May attempt further financial exploitation "
            "or request banking credentials"
        )

    elif stage == 3:

        next_move = (
            "May increase pressure to keep "
            "the conversation secret"
        )

    elif stage == 2:

        next_move = (
            "May escalate threats or intimidation"
        )

    elif stage == 1:

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
        "level": level,
        "score": score,
        "scam_type": scam_type,
        "stage": stage,
        "claim": claim,
        "proof": False,
        "reasons": reasons,
        "next_move": next_move
    }


# ==========================================
# 4. ROOT ENDPOINT
# ==========================================

@app.get("/")
def home():

    return {
        "message": "ScamBreaker P2 Detection API is running"
    }