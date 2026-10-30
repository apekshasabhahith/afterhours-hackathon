import json
from pathlib import Path
from faster_whisper import WhisperModel

def transcribe_audio(audio_path):

```
audio_file = Path(audio_path)

if not audio_file.exists():
    print("Error: Audio file not found!")
    return

print("\nLoading Whisper AI model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("\nTranscribing audio...")

segments, info = model.transcribe(
    str(audio_file),
    beam_size=5,
    vad_filter=True
)

transcript_parts = []

print("\nDetected Language:", info.language)
print("\n----- TRANSCRIPT -----\n")

for segment in segments:
    text = segment.text.strip()
    print(text)
    transcript_parts.append(text)

transcript = " ".join(transcript_parts)

# Save transcript as text
Path("transcript.txt").write_text(
    transcript,
    encoding="utf-8"
)

# Create JSON for Person 2
output = {
    "session_id": "demo_001",
    "language": info.language,
    "transcript": transcript
}

Path("transcript.json").write_text(
    json.dumps(output, ensure_ascii=False, indent=4),
    encoding="utf-8"
)

print("\nTranscript saved successfully!")
print("JSON file created for Person 2!")

return transcript
```

if **name** == "**main**":

```
print("================================")
print("   SCAMBREAKER AUDIO MODULE")
print("================================")

audio_path = input(
    "\nEnter your audio file name or path: "
).strip().strip('"')

transcribe_audio(audio_path)
```
