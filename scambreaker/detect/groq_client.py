import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from groq import Groq


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")


# ---------------------------------------------------------
# Create HTTP client
# ---------------------------------------------------------

http_client = httpx.Client(
    timeout=30.0
)


# ---------------------------------------------------------
# Create Groq client
# ---------------------------------------------------------

client = Groq(
    api_key=api_key,
    http_client=http_client
) if api_key else None


# ---------------------------------------------------------
# Check Groq availability
# ---------------------------------------------------------

def is_groq_available():
    return client is not None


# ---------------------------------------------------------
# Test Groq connection
# ---------------------------------------------------------

def test_groq():

    if client is None:
        return "Groq API key not configured."

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": "Reply with exactly: Groq connection successful"
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as error:

        return f"Groq connection failed: {error}"


# ---------------------------------------------------------
# Analyze message using Groq
# ---------------------------------------------------------

def analyze_with_groq(text):
    """
    Analyze a scam message using Groq.

    Returns None if Groq is unavailable or the request fails,
    so the rule-based detector can continue working.
    """

    if client is None:
        return None

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a scam detection assistant. "
                        "Analyze the user's message and briefly explain "
                        "whether it contains suspicious scam behavior. "
                        "Focus on authority impersonation, threats, isolation, "
                        "urgency, and financial requests."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception:
        return None