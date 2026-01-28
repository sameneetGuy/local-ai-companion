# Architecture

This project is a local PC-based voice companion with a simple pipeline:

Wake Word / PTT
→ Voice Capture
→ VAD (end-of-speech)
→ ASR (faster-whisper)
→ LLM (Ollama HTTP)
→ TTS (Piper)
→ Audio Playback

## Modules

- `main.py`
  - Main event loop
  - Wake word detection + Push-to-Talk fallback
  - Orchestrates one full interaction turn

- `audio_io.py`
  - Microphone capture (16 kHz mono int16 blocks)

- `vad.py`
  - WebRTC VAD-based recording:
    - waits for speech start
    - stops after silence threshold
    - enforces max recording time

- `asr.py`
  - Speech-to-text using `faster-whisper`

- `llm_ollama.py`
  - Local LLM via Ollama’s HTTP API (`/api/chat`)
  - Maintains a short conversation history

- `tts_piper.py`
  - Text-to-speech via Piper voice models (`.onnx` + `.onnx.json`)

- `config.py`
  - Central config for thresholds, devices, model choices, and endpoints

## Design goals

- Fully local by default (no cloud APIs required)
- Modular components (swap ASR/LLM/TTS backends without rewriting the app)
- Clear “turn-based” interaction (wake/PTT → record → respond)

## Future improvements (ideas)

- Better ASR reliability: fixed language, noise handling, confidence gating
- Hot-swappable voices / auto language switching
- UI/avatar layer (optional)
- Plugin-style “skills” (weather, music, smart home, etc.)
