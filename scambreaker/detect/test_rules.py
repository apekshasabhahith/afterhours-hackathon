from rules import detect_rules

test_messages = [
    "I am calling from CBI. You will be arrested. Transfer money immediately.",
    "Your bank branch will remain closed tomorrow.",
    "Do not disconnect. Do not tell your family.",
    "Tell me your OTP immediately.",
    "Hello, how are you? Have a nice day."
]

for message in test_messages:
    score, reasons = detect_rules(message)

    print("\nMessage:", message)
    print("Score:", score)
    print("Reasons:", reasons)