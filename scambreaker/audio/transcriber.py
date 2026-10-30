from faster_whisper import WhisperModel
import json

def transcribe_audio(audio_path):

    print("\nLoading Faster-Whisper model...")

    model = WhisperModel(
        "base",
        device="cpu",
        compute_type="int8"
    )

    print("Model loaded!")
    print("Transcribing audio...\n")

    segments, info = model.transcribe(
        audio_path,
        beam_size=5
    )

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

    with open("transcript.json", "w", encoding="utf-8") as file:
        json.dump(transcript, file, indent=4)

    print("\nTranscription completed!")
    print("Saved as transcript.json")

    return transcript


if __name__ == "__main__":

    transcribe_audio("test_audio.wav")