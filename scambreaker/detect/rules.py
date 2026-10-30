import re

AUTHORITY_KEYWORDS = [
    "cbi",
    "police",
    "rbi",
    "officer",
    "government",
    "customs department",
    "investigation bureau",
    "bank official"
]

THREAT_KEYWORDS = [
    "arrest",
    "jail",
    "warrant",
    "criminal case",
    "legal action",
    "account will be blocked",
    "freeze your account",
    "court case"
]

ISOLATION_KEYWORDS = [
    "don't tell anyone",
    "do not tell anyone",
    "don't inform your family",
    "do not inform your family",
    "don't disconnect",
    "do not disconnect",
    "don't contact anyone",
    "do not contact anyone",
    "stay on the call",
    "keep this confidential"
]

FINANCIAL_KEYWORDS = [
    "transfer money",
    "send money",
    "pay immediately",
    "registration fee",
    "verification fee",
    "bank otp",
    "share your otp",
    "tell me your otp",
    "tell me the otp",
    "otp you just received",
    "upi pin",
    "bank password",
    "personal account",
    "immediate payment",
    "money transfer"
]


def detect_rules(text):
    text = text.lower()

    score = 0
    reasons = []

    # -----------------------------
    # Authority impersonation
    # -----------------------------
    authority_contexts = [
        "i am calling from",
        "i am from",
        "calling from",
        "this is",
        "speaking from",
        "i am a",
        "i am an"
    ]

    authority_detected = any(
        context in text
        and any(keyword in text for keyword in AUTHORITY_KEYWORDS)
        for context in authority_contexts
    )

    if authority_detected:
        score += 20
        reasons.append("Authority impersonation detected")

    # -----------------------------
    # Threat / intimidation
    # -----------------------------
    if any(keyword in text for keyword in THREAT_KEYWORDS):
        score += 20
        reasons.append("Threat or intimidation detected")

    # -----------------------------
    # Isolation / secrecy
    # -----------------------------
    if any(keyword in text for keyword in ISOLATION_KEYWORDS):
        score += 25
        reasons.append("Isolation or secrecy detected")

    # -----------------------------
    # Financial exploitation
    # -----------------------------
    if any(keyword in text for keyword in FINANCIAL_KEYWORDS):
        score += 30
        reasons.append("Financial exploitation detected")

    # Maximum score = 100
    score = min(score, 100)

    return score, reasons