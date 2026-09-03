from challenge import generate_challenge, verify_challenge
from realtime_recorder import record_voice
from voice_to_text import transcribe


def authenticate():

    print("\n" + "=" * 45)
    print("🔐 VOICE AUTHENTICATION PROTOTYPE")
    print("=" * 45)

    challenge = generate_challenge()

    print(f'\n🗣️ Please say:\n"{challenge.upper()}"')

    audio_file = record_voice()

    if audio_file is None:
        print("\n❌ No speech detected.")
        return

    spoken_text = transcribe(audio_file)

    print(f"\n📝 You said: {spoken_text}")

    if verify_challenge(challenge, spoken_text):
        print("\n✅ AUTHENTICATION SUCCESSFUL!")
    else:
        print("\n❌ AUTHENTICATION FAILED!")
        print(f"Expected: {challenge}")
        print(f"Received: {spoken_text}")


def main():

    print("🚀 Starting Voice Authentication System...")
    print("🧠 Loading AI model once. Please wait...\n")

    while True:

        authenticate()

        choice = input(
            "\nPress ENTER to authenticate again "
            "or type 'q' to quit: "
        )

        if choice.lower() == "q":
            print("\n👋 Voice Authentication System stopped.")
            break


if __name__ == "__main__":
    main()