import sounddevice as sd
import wave

SAMPLE_RATE = 16000
DURATION = 5

print("Default devices:", sd.default.device)

print("🎤 Recording starts in 2 seconds...")
sd.sleep(2000)

print("🔴 Speak now!")

audio = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=1,
    dtype="int16"
)

sd.wait()

print("✅ Recording finished!")

with wave.open("test.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(audio.tobytes())

print("💾 Saved as test.wav")