import sounddevice as sd
import soundfile as sf

# Audio settings
DURATION = 30
SAMPLE_RATE = 16000
CHANNELS = 1

def record_audio():

    print("\nSCAMBREAKER AUDIO RECORDER")
    print("--------------------------")

    print("Recording will start in 2 seconds...")
    import time
    time.sleep(2)

    print("Recording started! Speak now...")

    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS
    )

    sd.wait()

    print("Recording completed!")

    sf.write(
        "test_audio.wav",
        audio,
        SAMPLE_RATE
    )

    print("Audio saved successfully!")
    print("File: test_audio.wav")


if __name__ == "__main__":
    record_audio()