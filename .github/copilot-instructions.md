# Copilot instructions for Voice-auth

## Build, test, and validation

There is no formal build system, linter configuration, or CI workflow checked into this repository.

Use the project virtual environment before running Python code:

```bash
source venv/bin/activate
```

Relevant commands that are already part of the workflow:

```bash
# Run the main prototype flow
python src/main.py

# Transcribe an existing WAV file (smoke test)
python src/voice_to_text.py

# Record a fresh sample with the microphone
python src/realtime_recorder.py

# Run an individual test script
python -m pytest tests/speech_test.py -q
```

The `tests/` folder contains hardware/audio probe scripts rather than a standard unit-test suite. `mic_test.py`, `record_test.py`, and `speech_test.py` are intended for local validation of microphone access and audio transcription on this machine.

## High-level architecture

This repo is a prototype Linux voice-authentication pipeline, not a production authentication system.

Current flow:

```text
Microphone -> Silero VAD -> recorded WAV -> Faster-Whisper -> text -> challenge verification
```

Key files:

- `src/realtime_recorder.py`: captures microphone input, uses Silero VAD to detect speech, and saves the spoken audio as a WAV file in `recordings/realtime_voice.wav`.
- `src/voice_to_text.py`: loads the Faster-Whisper model and converts recorded audio into text.
- `src/challenge.py`: challenge-response prototype for matching spoken words to a generated challenge phrase. This is a shelved experiment, not the current MVP core.
- `src/main.py`: orchestrates the prototype flow and loops through challenge authentication.
- `tests/*.py`: local validation scripts for microphone access, recording, and transcription.

The project goal in `README.md` is intentionally narrow: prove the voice pipeline works first, and only add complexity after the basic path is stable. The final Ubuntu unlock integration is not connected yet.

## Key conventions and repo-specific expectations

- Keep the MVP simple. The README explicitly says not to add speaker verification, anti-replay controls, liveness checks, or PAM/GDM work before the basic voice pipeline is proven.
- Treat these modules as script-oriented tooling, not as a framework. Most logic is in top-level functions and direct imports rather than a layered app structure.
- Audio is handled as local WAV files and Linux audio-device I/O, so behavior depends on the host machine's microphone and sound stack (`sounddevice`, PipeWire/PulseAudio compatibility).
- Imports are written as if the project is run from the repository root or from within `src` in a way that preserves the local package path. Avoid introducing package layout changes unless the repo explicitly adopts a packaging structure.
- The repository currently stores recorded audio in `recordings/` and uses root-level `test.wav` for transcription smoke tests.
- Prefer surgical, prototype-friendly changes over broad architecture churn; this codebase is still in the early proof-of-concept phase.

## Practical guidance for future Copilot sessions

- When making changes, keep the system focused on the voice pipeline and challenge verification path.
- Preserve the explicit project scope described in `README.md`: basic recognition first, advanced security features later.
- When validating changes, favor the smallest practical audio/test command rather than assuming a formal CI pipeline exists.
