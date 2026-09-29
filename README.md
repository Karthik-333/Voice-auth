# Voice-Auth

A Linux voice-authentication project for unlocking Ubuntu using a spoken
voice command.

> **Current project goal:** Build a simple, reliable voice-unlock MVP
> first. Advanced security, speaker verification, anti-replay
> protection, and other enhancements will be added only after the core
> system works.

------------------------------------------------------------------------

## 1. Project Goal

The long-term goal is to allow the user to unlock Ubuntu using voice
instead of typing the password every time.

The intended experience is:

``` text
Ubuntu locked
     ↓
🎤 Listen
     ↓
Speech detected
     ↓
Speech → Text
     ↓
Recognize an unlock command
     ↓
🔓 Unlock Ubuntu
```

For the current MVP, the system will **not modify Ubuntu authentication
yet**.

The first milestone is simply proving that the system can reliably
recognize an unlock command.

------------------------------------------------------------------------

# 2. Development Philosophy

This project follows a simple rule:

> **Make the basic system work first. Add complexity only when the
> previous layer is stable.**

We intentionally avoid adding the following during the initial MVP:

-   Random challenge phrases
-   Numbers/challenge-response authentication
-   Speaker verification
-   Voice embeddings
-   Liveness detection
-   Anti-replay mechanisms
-   Complex AI-agent pipelines
-   PAM/GDM modifications before the voice pipeline is proven

These are future enhancements, not current requirements.

------------------------------------------------------------------------

# 3. Current Architecture

The current voice pipeline is:

``` text
                 VOICE-AUTH
                     │
                     ▼
              🎤 Microphone
                     │
                     ▼
              Silero VAD
          "Is someone speaking?"
                     │
                     ▼
             Voice Recorder
                     │
                     ▼
             Faster-Whisper
          Speech → Text
                     │
                     ▼
          Command Recognition
                     │
                     ▼
       "unlock my computer"
                     │
                     ▼
              🔓 Unlock
```

The final unlock mechanism is **not connected yet**.

------------------------------------------------------------------------

# 4. Technology Stack

  Component                  Technology                            Purpose
  -------------------------- ------------------------------------- ----------------------------
  Operating System           Ubuntu 26.04.1 LTS                    Target OS
  Desktop                    Ubuntu GNOME                          Target desktop environment
  Audio                      PipeWire + PulseAudio compatibility   System audio
  Microphone access          `sounddevice`                         Capture microphone audio
  Numerical processing       `numpy`                               Audio array processing
  Voice Activity Detection   Silero VAD                            Detect speech and silence
  Speech Recognition         Faster-Whisper                        Convert speech into text
  Language                   Python                                Main development language
  Environment                Python virtual environment            Dependency isolation

------------------------------------------------------------------------

# 5. Project Structure

Current structure:

``` text
voice-auth/
│
├── venv/
│
├── tests/
│   ├── mic_test.py
│   ├── record_test.py
│   └── speech_test.py
│
├── recordings/
│
└── src/
    ├── realtime_recorder.py
    ├── voice_to_text.py
    ├── challenge.py
    └── main.py
```

### File responsibilities

#### `tests/mic_test.py`

Used to inspect available audio devices and verify microphone access.

#### `tests/record_test.py`

Used to perform basic fixed-duration microphone recording.

#### `tests/speech_test.py`

Used to test Faster-Whisper independently.

#### `src/realtime_recorder.py`

Responsible for:

-   Listening to the microphone
-   Processing audio in chunks
-   Detecting speech using Silero VAD
-   Detecting when the user stops speaking
-   Saving the captured speech as WAV audio

#### `src/voice_to_text.py`

Responsible for:

-   Loading Faster-Whisper
-   Receiving recorded audio
-   Converting speech into text

Current model:

``` text
Whisper small
```

Current configuration uses English recognition:

``` python
language="en"
```

along with:

``` python
beam_size=1
vad_filter=True
condition_on_previous_text=False
```

#### `src/challenge.py`

Previously created for challenge-response experiments.

It is currently **shelved** and is not part of the MVP.

#### `src/main.py`

Will become the main application entry point.

Its immediate responsibility is to connect:

``` text
Recorder → Whisper → Command Recognition
```

------------------------------------------------------------------------

# 6. Completed Work

## Phase 0 --- Environment Setup

### Completed

-   Ubuntu environment verified
-   Python environment created
-   Virtual environment created
-   Audio libraries installed
-   Faster-Whisper installed
-   Silero VAD installed
-   PortAudio development dependency installed

------------------------------------------------------------------------

## Phase 1A --- Microphone Testing

### Goal

Verify that Python can access the microphone.

### Result

Completed successfully.

The built-in microphone works correctly.

We initially experimented with a hardcoded PortAudio device ID, but
device indices are not stable enough to depend on.

The implementation was changed to use the system/default input device.

### Status

**✅ Complete**

------------------------------------------------------------------------

## Phase 1B --- Basic Audio Recording

### Goal

Capture microphone audio and save it as a WAV file.

Configuration:

``` text
Sample rate: 16 kHz
Channels:    Mono
Format:      WAV
```

### Result

Recording works correctly and the recorded voice is clearly audible.

There is a small amount of background noise, but it is acceptable for
the MVP.

### Status

**✅ Complete**

------------------------------------------------------------------------

## Phase 1C --- Speech-to-Text

### Goal

Convert recorded speech into text.

Technology:

``` text
Faster-Whisper
```

Model:

``` text
small
```

### Result

Normal speech is successfully transcribed.

We also discovered that the model could occasionally:

-   Misrecognize short words
-   Detect the wrong language
-   Take significant time to load

The language configuration was changed to explicitly use English.

### Known performance issue

The Whisper `small` model currently takes approximately 45--60 seconds
to initially load on the development machine.

This is considered a **startup/performance issue**, not a reason to
redesign the MVP.

Later, the model will remain loaded in a persistent background service.

### Status

**✅ Core functionality complete**

**🟡 Performance optimization deferred**

------------------------------------------------------------------------

# 7. Phase 1D --- Voice Activity Detection

## Why VAD?

A voice-unlock system should not require the user to press a recording
button.

Instead:

``` text
Wait for speech
     ↓
Start recording
     ↓
User speaks
     ↓
Detect silence
     ↓
Stop recording
```

Silero VAD is used for this purpose.

------------------------------------------------------------------------

## Current behavior

The recorder processes audio in chunks.

Current chunk duration:

``` text
0.5 seconds
```

The system:

1.  Waits for speech
2.  Detects speech
3.  Starts collecting audio
4.  Continues while speech is present
5.  Stops after approximately 1.5 seconds of silence
6.  Saves the recording

A maximum waiting time prevents the program from listening forever when
no speech is detected.

### Result

The real-time recorder was tested successfully.

### Status

**✅ Complete**

------------------------------------------------------------------------

# 8. Phase 1E --- Connected Voice Pipeline

The recorder and Whisper have been connected.

Current pipeline:

``` text
🎤 Microphone
      ↓
Silero VAD
      ↓
Real-time recording
      ↓
WAV file
      ↓
Faster-Whisper
      ↓
Transcribed text
```

The recorder returns the audio filename when recording succeeds and
returns `None` when no speech is detected.

This allows the main program to control the pipeline safely.

### Status

**✅ Complete**

------------------------------------------------------------------------

# 9. Current MVP

The immediate MVP is:

``` text
🎤 User speaks
       ↓
Silero VAD detects speech
       ↓
Audio recorded
       ↓
Whisper transcribes it
       ↓
Normalize text
       ↓
Check unlock command
       ↓
✅ Command recognized
```

Example:

``` text
User:
"unlock my computer"

Whisper:
"unlock my computer"

Application:
✅ Unlock command recognized
```

At this stage:

``` text
❌ Ubuntu is NOT unlocked
```

The application only proves that the command was recognized.

This is intentional.

------------------------------------------------------------------------

# 10. Immediate Next Step

## Command Recognition

The next implementation should connect the existing modules through
`main.py`.

Target flow:

``` text
START
  ↓
Load VAD
  ↓
Load Whisper
  ↓
🎤 Listen
  ↓
Detect speech
  ↓
Record speech
  ↓
Transcribe
  ↓
Normalize text
  ↓
Check unlock command
  ├── Match → ✅ Command recognized
  └── No match → ❌ Command not recognized
```

For the first version, use a simple fixed command such as:

``` text
unlock my computer
```

A small number of natural variants can be supported later if necessary.

Do not introduce fuzzy matching, random challenges, or speaker
verification unless there is a demonstrated need.

------------------------------------------------------------------------

# 11. Full Development Roadmap

## Phase 1 --- Voice Command MVP

### Objective

Prove that the system can recognize a spoken unlock command.

### Tasks

-   [x] Microphone access
-   [x] Basic recording
-   [x] Faster-Whisper integration
-   [x] Silero VAD integration
-   [x] Real-time recording
-   [x] Connect recorder to Whisper
-   [ ] Implement command recognition
-   [ ] Test the complete voice-command flow
-   [ ] Handle no-speech cases
-   [ ] Handle unrecognized commands

### Success criteria

The application should reliably perform:

``` text
Speak
  ↓
Record
  ↓
Transcribe
  ↓
Recognize unlock command
  ↓
Print success
```

------------------------------------------------------------------------

# 12. Phase 2 --- Persistent Background Service

The current development application starts manually.

That is not suitable for a real unlock system.

The next architecture will be:

``` text
Ubuntu starts
     ↓
Voice-Auth service starts
     ↓
Load Silero VAD
     ↓
Load Whisper
     ↓
Keep models in memory
     ↓
Wait for voice input
```

### Why?

The Whisper model currently takes approximately 45--60 seconds to load.

We do not want:

``` text
User wants to unlock
       ↓
Start program
       ↓
Wait 60 seconds
       ↓
Load model
       ↓
Listen
```

Instead:

``` text
Ubuntu starts
       ↓
Voice-Auth starts in background
       ↓
Whisper already loaded
       ↓
User speaks
       ↓
Process immediately
```

### Tasks

-   [ ] Create a long-running application process
-   [ ] Keep VAD model loaded
-   [ ] Keep Whisper model loaded
-   [ ] Measure recognition latency
-   [ ] Measure CPU and memory usage
-   [ ] Create a system service
-   [ ] Start service automatically

### Success criteria

Voice-Auth remains ready in the background without requiring manual
startup.

------------------------------------------------------------------------

# 13. Phase 3 --- Ubuntu Lock-Screen Integration

Only after the voice-command system and background service are stable.

Goal:

``` text
Ubuntu locked
      ↓
Voice-Auth
      ↓
Voice command recognized
      ↓
Authentication integration
      ↓
🔓 Ubuntu unlocked
```

Before implementation, investigate the correct authentication
architecture for:

``` text
Ubuntu 26.04.1 LTS
Ubuntu GNOME
GDM
PAM
```

Do not blindly modify PAM configuration.

Authentication changes can lock the user out if configured incorrectly.

The implementation should maintain:

``` text
Voice authentication
        +
Password fallback
```

------------------------------------------------------------------------

# 14. Phase 4 --- Performance Optimization

Once the system actually works end-to-end, optimize it.

Potential areas:

### Model loading

Keep Whisper loaded rather than loading it for every request.

### Latency

Measure:

``` text
Speech starts
      ↓
VAD detects speech
      ↓
Speech ends
      ↓
Transcription starts
      ↓
Transcription finishes
      ↓
Command recognized
```

### CPU usage

Monitor idle CPU usage while waiting for speech.

### Memory usage

Monitor the memory consumed by:

-   Whisper
-   Silero VAD
-   Python
-   Audio buffers

### Audio processing

Investigate:

-   Noise suppression
-   Better microphone preprocessing
-   Appropriate VAD thresholds
-   Recording buffer optimization

------------------------------------------------------------------------

# 15. Phase 5 --- Accuracy Improvements

After the basic system works, improve recognition quality.

Potential improvements:

``` text
Microphone calibration
        ↓
Noise suppression
        ↓
Better preprocessing
        ↓
Command normalization
        ↓
Command matching
```

Possible Whisper improvements can include:

-   Model configuration
-   Language configuration
-   Beam-search settings
-   VAD filtering
-   Audio preprocessing
-   Potentially testing a lighter model

------------------------------------------------------------------------

# 16. Important Architectural Question --- Do We Really Need Whisper?

Whisper is useful for the MVP because it gives us a simple:

``` text
Speech → Text
```

pipeline.

However, the final system may only need to recognize a very small set of
commands.

For example:

``` text
"unlock my computer"
"unlock computer"
"unlock Ubuntu"
```

A general-purpose speech-to-text model may be more than we need.

A future architecture could be:

``` text
Voice
  ↓
Voice-command recognition
  ↓
Known command
  ↓
Authentication
```

instead of:

``` text
Voice
  ↓
General speech-to-text
  ↓
Text processing
  ↓
Command recognition
  ↓
Authentication
```

But this decision should be made **after the MVP works**, based on
actual performance.

Do not optimize this prematurely.

------------------------------------------------------------------------

# 17. Phase 6 --- Security

The current MVP is **not yet a secure authentication system**.

It primarily proves voice command recognition.

A real authentication system needs to answer two different questions:

### Question 1

> What did the user say?

This is speech recognition.

### Question 2

> Who said it?

This is speaker verification.

Whisper primarily solves the first problem.

Future security work can address the second.

------------------------------------------------------------------------

## Future security features

### Speaker verification

Determine whether the voice belongs to the authorized user.

Possible architecture:

``` text
Microphone
    ↓
Voice activity detection
    ↓
Speech
    ↓
Speaker embedding
    ↓
Compare against enrolled voice
    ↓
Authorized?
```

------------------------------------------------------------------------

### Anti-replay protection

Protect against someone playing a recording of the authorized user's
voice.

------------------------------------------------------------------------

### Liveness detection

Determine whether the input is coming from a live speaker rather than a
replayed recording.

------------------------------------------------------------------------

### Secure credential handling

Never store the user's actual Ubuntu password in plain text.

The voice system should not expose or log sensitive authentication
material.

------------------------------------------------------------------------

# 18. Challenge-Response

Challenge-response was previously considered.

Example:

``` text
System:
"Say: golden falcon 33"

User:
"golden falcon 33"
```

This can help with replay resistance.

However:

``` text
CURRENT STATUS: 🟡 DEFERRED
```

It is intentionally not part of the initial MVP.

We will revisit it only if the security design requires it.

------------------------------------------------------------------------

# 19. Security Model --- Future

The eventual system should look more like:

``` text
                 🎤 Voice
                    │
                    ▼
              Silero VAD
                    │
                    ▼
             Audio Processing
                    │
             ┌──────┴──────┐
             ▼             ▼
        Speech-to-Text   Speaker
             │           Verification
             │             │
             └──────┬──────┘
                    ▼
             Security Checks
                    │
             ┌──────┴──────┐
             │             │
          Authorized?    Replay?
             │             │
             └──────┬──────┘
                    ▼
             Authentication
                    │
                    ▼
                  🔓
```

This is a **future architecture**, not the current implementation.

------------------------------------------------------------------------

# 20. Testing Strategy

Testing will be incremental.

## Current testing

### Microphone

Verify:

``` text
Can Python access the microphone?
```

### Recording

Verify:

``` text
Can we capture usable audio?
```

### VAD

Verify:

``` text
Can the system detect speech and silence?
```

### Whisper

Verify:

``` text
Can speech be converted into text?
```

### Integrated pipeline

Verify:

``` text
Can microphone input become text automatically?
```

------------------------------------------------------------------------

## Future testing

After command recognition:

``` text
Command recognized correctly
Command rejected correctly
No speech handled
Background noise handled
Long silence handled
Multiple attempts handled
```

After Ubuntu integration:

``` text
Voice unlock works
Password fallback works
Incorrect voice command does not unlock
Service restarts correctly
System boot remains usable
```

------------------------------------------------------------------------

# 21. Failure Handling

The application should fail safely.

Examples:

### No speech

``` text
🎤 Listening...
❌ No speech detected
```

Then return to listening.

### Unrecognized command

``` text
❌ Command not recognized
```

Do not unlock.

### Whisper failure

``` text
❌ Speech recognition failed
```

Do not unlock.

### Authentication failure

Fall back to the normal Ubuntu password mechanism.

------------------------------------------------------------------------

# 22. Design Principles

The project should follow these principles throughout development:

### 1. MVP first

Do not add security mechanisms before the basic system works.

### 2. Small incremental changes

Change one major component at a time.

### 3. Test before moving forward

Every phase should have a clear success condition.

### 4. Fail closed

If recognition or authentication is uncertain:

``` text
Do NOT unlock.
```

### 5. Keep password fallback

Voice authentication should initially be an additional authentication
path, not the only way to access the system.

### 6. Avoid unnecessary AI complexity

Use AI where it solves a real problem.

### 7. Optimize after functionality

Do not prematurely optimize Whisper/model architecture.

------------------------------------------------------------------------

# 23. Milestones

  Milestone   Goal                             Status
  ----------- -------------------------------- -------------
  M1          Microphone access                ✅ Complete
  M2          Basic recording                  ✅ Complete
  M3          Whisper transcription            ✅ Complete
  M4          Silero VAD                       ✅ Complete
  M5          Real-time recording              ✅ Complete
  M6          VAD → Whisper pipeline           ✅ Complete
  M7          Voice command recognition        🔵 Current
  M8          Persistent background service    ⏳ Planned
  M9          Ubuntu lock-screen integration   ⏳ Planned
  M10         Performance optimization         ⏳ Planned
  M11         Accuracy improvements            ⏳ Planned
  M12         Speaker verification             ⏳ Future
  M13         Anti-replay/liveness             ⏳ Future
  M14         Production security review       ⏳ Future

------------------------------------------------------------------------

# 24. Current Definition of Done

The current MVP is complete when:

``` text
1. Start Voice-Auth
        ↓
2. System listens automatically
        ↓
3. User speaks
        ↓
4. Silero VAD detects speech
        ↓
5. Speech is recorded
        ↓
6. Whisper transcribes it
        ↓
7. Command is recognized
        ↓
8. Application confirms:
   "Unlock command recognized"
```

Only after this works consistently should we proceed to Ubuntu
authentication integration.

------------------------------------------------------------------------

# 25. Final Target

The eventual finished system should provide:

``` text
                 Ubuntu
                    │
                    ▼
              🔒 Locked
                    │
                    ▼
             Voice-Auth Service
                    │
                    ▼
              🎤 User speaks
                    │
                    ▼
             Speech Detection
                    │
                    ▼
            Voice Recognition
                    │
                    ▼
          Speaker Verification
                    │
                    ▼
             Security Checks
                    │
              ┌─────┴─────┐
              │           │
           Valid        Invalid
              │           │
              ▼           ▼
            🔓        🔒 Remain locked
```

with:

``` text
Password
   ↓
Fallback authentication
```

always available.

------------------------------------------------------------------------

# 26. Current Focus

> ## 🎯 DO NOT JUMP AHEAD

The only thing we should work on right now is:

``` text
🎤 Voice
   ↓
Silero VAD
   ↓
Recording
   ↓
Whisper
   ↓
"unlock my computer"
   ↓
✅ Command recognized
```

Once this works, move to the background service.

Then move to Ubuntu integration.

Then optimize.

Then improve security.

------------------------------------------------------------------------

## Project Status

**Current phase:** Phase 1 --- Voice Command MVP

**Current task:** Implement command recognition in `main.py`

**Next major milestone:** Persistent background voice-auth service

**Ultimate goal:** Secure voice-assisted Ubuntu unlocking with password
fallback.
