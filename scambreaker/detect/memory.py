# ScamBreaker - Conversation Memory

class ConversationMemory:

    def __init__(self):
        self.calls = {}

    def update(self, call_id, text, score, reasons, stage):

        if call_id not in self.calls:
            self.calls[call_id] = {
                "score": 0,
                "messages": set(),
                "reasons": [],
                "stage": 0
            }

        call = self.calls[call_id]

        # Avoid duplicate scoring
        normalized_text = text.lower().strip()

        if normalized_text in call["messages"]:
            return call

        call["messages"].add(normalized_text)

        # Cumulative risk score
        call["score"] = min(
            100,
            call["score"] + score
        )

        # Store unique reasons
        for reason in reasons:
            if reason not in call["reasons"]:
                call["reasons"].append(reason)

        # Track highest stage
        call["stage"] = max(
            call["stage"],
            stage
        )

        return call

    def reset(self, call_id):
        self.calls.pop(call_id, None)
        return {"message": "Conversation reset"}