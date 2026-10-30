from faster_whisper import WhisperModel
import json
import requests


# ---------------------------------------------------------
# P2 Backend URL
# ---------------------------------------------------------

P2_URL = "http://localhost:8002/analyze"


# ---------------------------------------------------------
# Transcribe Audio
# ---------------------------------------------------------

def transcribe_audio(audio_path, language=None):

    print("\nLoading Faster-Whisper model...")

    model = WhisperModel(
        "small",
        device="cpu",
        compute_type="int8"
    )

    print("Model loaded!")
    print("Transcribing audio...\n")

    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        language="mr",
        task="translate"
    )

    print("Detected language:", info.language)

    transcript = []

    for segment in segments:

        text = segment.text.strip()

        result = {
            "text": text,
            "ts": round(segment.start, 2),
            "call_id": "demo"
        }

        transcript.append(result)

        print(f"[{segment.start:.2f}s] {text}")

        # -------------------------------------------------
        # Send transcript segment to P2
        # -------------------------------------------------

        try:

            response = requests.post(
                P2_URL,
                json=result,
                timeout=10
            )

            if response.status_code == 200:

                analysis = response.json()

                print("\n----- P2 SCAM ANALYSIS -----")
                print("Risk Level :", analysis["level"])
                print("Score      :", analysis["score"])
                print("Scam Type  :", analysis["scam_type"])
                print("Stage      :", analysis["stage"])
                print("Claim      :", analysis["claim"])
                print("Reasons    :", analysis["reasons"])
                print("Next Move  :", analysis["next_move"])
                print("----------------------------\n")

            else:

                print(
                    "P2 returned error:",
                    response.status_code,
                    response.text
                )

        except requests.exceptions.RequestException as error:

            print("Could not connect to P2:", error)

    # -----------------------------------------------------
    # Save transcript
    # -----------------------------------------------------

    with open("transcript.json", "w", encoding="utf-8") as file:

        json.dump(
            transcript,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nTranscription completed!")
    print("Saved as transcript.json")

    return transcript


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    transcribe_audio(
        "test_audio.wav",
        language=None
    )