import requests

P2_URL = "http://localhost:8002/analyze"

messages = [
    "I am calling from the CBI.",
    "Your bank account is involved in a criminal case.",
    "Do not tell your family and stay on the call.",
    "You must transfer money immediately and tell me the OTP."
]

for i, text in enumerate(messages):

    data = {
        "text": text,
        "ts": float(i),
        "call_id": "demo"
    }

    print("\nP1 -> P2")
    print("Transcript:", text)

    try:
        response = requests.post(
            P2_URL,
            json=data,
            timeout=10
        )

        print("Status:", response.status_code)

        if response.status_code == 200:

            result = response.json()

            print("\n----- P2 SCAM ANALYSIS -----")
            print("Risk Level :", result["level"])
            print("Score      :", result["score"])
            print("Scam Type  :", result["scam_type"])
            print("Stage      :", result["stage"])
            print("Claim      :", result["claim"])
            print("Reasons    :", result["reasons"])
            print("Next Move  :", result["next_move"])
            print("----------------------------")

        else:
            print("P2 Error:", response.text)

    except Exception as error:
        print("Connection failed:", error)