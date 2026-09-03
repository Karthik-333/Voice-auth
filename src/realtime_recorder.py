import sounddevice as sd
import numpy as np
import wave
import time

from silero_vad import load_silero_vad, get_speech_timestamps


SAMPLE_RATE = 16000
CHANNELS = 1

CHUNK_DURATION = 0.5
CHUNK_SAMPLES = int(SAMPLE_RATE * CHUNK_DURATION)

MAX_WAIT_FOR_SPEECH = 10
SILENCE_TIMEOUT = 1.5


print("🧠 Loading Silero VAD...")
model = load_silero_vad()


def contains_speech(audio):

    timestamps = get_speech_timestamps(
        audio,
        model,
        sampling_rate=SAMPLE_RATE
    )

    return len(timestamps) > 0


def record_voice():

    print("\n🎤 Listening...")
    print("Start speaking...\n")

    recorded_chunks = []

    speech_started = False
    last_speech_time = None

    start_time = time.time()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="float32",
        blocksize=CHUNK_SAMPLES
    ) as stream:

        while True:

            audio, overflowed = stream.read(CHUNK_SAMPLES)

            audio = audio.flatten()

            has_speech = contains_speech(audio)

            current_time = time.time()

            # Wait for user to start speaking
            if not speech_started:

                if has_speech:
                    print("🗣️ Speech detected!")
                    speech_started = True
                    last_speech_time = current_time
                    recorded_chunks.append(audio)

                elif current_time - start_time > MAX_WAIT_FOR_SPEECH:
                    print("❌ No speech detected.")
                    return None

            else:

                recorded_chunks.append(audio)

                if has_speech:
                    last_speech_time = current_time

                # Stop after silence
                if current_time - last_speech_time > SILENCE_TIMEOUT:
                    print("🤫 Silence detected. Stopping...")
                    break


    if not recorded_chunks:
        return None

    final_audio = np.concatenate(recorded_chunks)

    # Convert safely to int16
    final_audio = np.clip(final_audio, -1.0, 1.0)
    final_audio_int16 = (final_audio * 32767).astype(np.int16)

    filename = "recordings/realtime_voice.wav"

    with wave.open(filename, "wb") as wf:

        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(final_audio_int16.tobytes())


    duration = len(final_audio) / SAMPLE_RATE

    print(f"✅ Recording saved: {filename}")
    print(f"⏱️ Duration: {duration:.2f} seconds")

    return filename

if __name__ == "__main__":
    record_voice()
