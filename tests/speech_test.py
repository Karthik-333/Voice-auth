from faster_whisper import WhisperModel

print("🧠 Loading speech recognition model...")

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

print("🎤 Transcribing your recording...\n")

segments, info = model.transcribe(
    "test.wav",
    beam_size=5
)

print("Detected language:", info.language)

print("\n📝 You said:")

for segment in segments:
    print(segment.text)
