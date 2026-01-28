# Local AI Companion

A fully local, open-source AI companion running on your PC, featuring:

- Wake word detection (OpenWakeWord)
- Push-to-Talk fallback
- Offline speech-to-text (faster-whisper)
- Local LLM via Ollama
- Offline text-to-speech (Piper)

No cloud APIs required.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
  - [Pull the LLM model](#pull-the-llm-model)
  - [Installation](#installation)
  - [Platform-specific notes](#platform-specific-notes)
    - [Windows](#windows)
    - [macOS](#macos)
    - [Linux](#linux)
  - [Piper voices (required)](#piper-voices-required)
  - [Configuration](#configuration)
  - [Run](#run)
  - [Notes](#notes)
  - [Third-party components and licenses](#third-party-components-and-licenses)
  - [License](#license)


## Features

- 🎙️ Wake word + Push-to-Talk (PTT)
- 🧠 Local LLM reasoning (Ollama)
- 🗣️ Offline ASR with Whisper
- 🔊 Offline TTS with Piper
- 🇺🇸 / 🇧🇷 Multiple voice support (en_US, pt_BR)
- 🧩 Modular, hackable Python architecture

---

## Prerequisites

- **Python 3.10+**
- **Ollama** installed and running  
  https://ollama.com

### Pull the LLM model
```
ollama run llama3.1:8b
```

### Installation
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Platform-specific notes

This project is designed to run on **Windows, macOS, and Linux**, but some system
dependencies and behaviors differ by OS.

#### Windows
- No additional system dependencies required.
- Push-to-Talk (PTT) uses the `keyboard` library and may require running the terminal
  as **Administrator**.

#### macOS
- Install PortAudio (required for microphone input):
  ```bash
  brew install portaudio
  ```
- The PTT hotkey backend uses pynput. macOS may prompt for Accessibility / Input Monitoring permissions the first time it runs.

### Linux
- Install PortAudio development headers:
 ```bash
 sudo apt-get update
 sudo apt-get install -y portaudio19-dev
 ```
- PTT uses pynput; behavior may vary slightly depending on desktop environment.
If Push-to-Talk is unavailable on your system, the companion will still work normally using wake word detection.


### Piper voices (required)
Create a voices/ folder and place Piper voice files inside:
```
voices/
  en_US-lessac-medium.onnx
  en_US-lessac-medium.onnx.json
  pt_BR-jeff-medium.onnx
  pt_BR-jeff-medium.onnx.json
```
Piper voices are available from the rhasspy/piper-voices repository (MIT-licensed).

### Configuration
Edit config.py to choose:
- Wake word behavior
- ASR language
- Active TTS voice (en_US or pt_BR)
- Ollama endpoint and model
Example:
```python
tts_voice = "pt_BR"
```

### Run
```
python main.py
```

### Notes
- First run may download OpenWakeWord models automatically
- Push-to-Talk uses the keyboard library and may require running the terminal as Administrator on Windows
- Ollama must be running in the background (ollama serve)

### Third-party components and licenses

This project depends on several third-party open-source projects.
Each component is distributed under its own license:

- **OpenWakeWord** – wake word detection  
- **faster-whisper** – speech-to-text (Whisper)  
- **Ollama** – local LLM runtime  
- **Piper** – text-to-speech engine  
- **ONNX Runtime** – model inference runtime  
See [here](./THIRD_PARTY_LICENSES.md) for details.

This repository contains **only original source code** for the companion logic.

No third-party models, weights, or binaries are redistributed as part of this repository.
Users are responsible for downloading and using third-party components in accordance
with their respective licenses.

### License
MIT License.

This project is intended to be fully open-source friendly.

All default components (OpenWakeWord, Whisper, Piper, Ollama) are locally hosted and redistributable under their respective licenses.

Optional proprietary or restricted TTS engines are intentionally not included.
