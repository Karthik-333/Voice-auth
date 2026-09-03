import sounddevice as sd
import numpy as np
import wave
from silero_vad import load_silero_vad, get_speech_timestamps


SAMPLE_RATE = 16000
CHANNELS = 1

# Load Silero VAD model
print("🧠 Loading Voice Activity Detection model...")
model = load_silero_vad()


def record_until_silence():
    print("\n🎤 Listening...")
    print("Start speaking whenever you're ready.\n")

    audio_chunks = []

    # Record maximum 15 seconds initially
    recording = sd.rec(
        int(15 * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32"
    )

    sd.wait()

    audio = recording.flatten()

    # Detect speech
    speech_timestamps = get_speech_timestamps(
        audio,
        model,
        sampling_rate=SAMPLE_RATE
    )

    if not speech_timestamps:
        print("❌ No speech detected.")
        return

    # Find speech boundaries
    start = speech_timestamps[0]["start"]
    end = speech_timestamps[-1]["end"]

    speech_audio = audio[start:end]

    print("✅ Speech detected!")
    print(f"Speech duration: {(end - start) / SAMPLE_RATE:.2f} seconds")

    # Convert to int16 for WAV
    speech_audio_int16 = (
        speech_audio * 32767
    ).astype(np.int16)

    filename = "recordings/voice.wav"

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(speech_audio_int16.tobytes())

    print(f"💾 Saved recording to {filename}")


if __name__ == "__main__":
    record_until_silence()
