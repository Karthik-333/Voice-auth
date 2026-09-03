from faster_whisper import WhisperModel
from realtime_recorder import record_voice


print("🧠 Loading Whisper model...")

model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def transcribe(audio_file):

    print("\n🧠 Transcribing...")

    segments, info = model.transcribe(
        audio_file,
        beam_size=5
    )

    text = ""

    for segment in segments:
        text += segment.text

    return text.strip()


if __name__ == "__main__":
    audio_file = record_voice()

    if audio_file is None:
        print("Authentication cancelled: no speech detected.")
    else:
        result = transcribe(audio_file)

        print("\n📝 You said:")
        print(result)