# config.py
from dataclasses import dataclass, field

@dataclass
class Config:
    # Audio
    sample_rate: int = 16000
    channels: int = 1
    block_ms: int = 20  # 10/20/30ms for webrtcvad
    input_device: str | None = None  # None = default

    # Wake word
    wakeword_threshold: float = 0.65
    wakeword_consecutive_hits: int = 3
    wakeword_cooldown_s: float = 2.5

    # PTT (Option C fallback)
    ptt_key: str = "right ctrl"  # requires `keyboard` lib (may need admin)

    # VAD (WebRTC VAD)
    vad_aggressiveness: int = 2  # 0..3 (higher = more aggressive)
    min_speech_ms: int = 250
    end_silence_ms: int = 900
    max_record_s: float = 15.0

    # ASR
    whisper_model: str = "medium"  # small / medium / large-v3 etc.
    whisper_device: str = "cpu"    # "cuda" if you set up GPU properly
    whisper_compute_type: str = "int8"  # int8 on CPU is common

    # LLM (Ollama)
    ollama_url: str = "http://127.0.0.1:11434/api/chat"
    ollama_model: str = "llama3.1:8b"
    system_prompt: str = (
        "You are a helpful, concise local AI companion. "
        "Keep responses short unless asked otherwise."
    )

    # TTS (Piper)
    tts_voice: str = "en_US"  # "en_US" or "pt_BR"
    piper_voices: dict = field(default_factory=lambda: {
        "en_US": {
            "model": "voices/en_US-lessac-medium.onnx",
            "config": "voices/en_US-lessac-medium.onnx.json",
        },
        "pt_BR": {
            "model": "voices/pt_BR-jeff-medium.onnx",
            "config": "voices/pt_BR-jeff-medium.onnx.json",
        },
    })
    # Optional: path to a reference speaker wav to clone. If None, uses default speaker.
    speaker_wav: str | None = None
    tts_language: str = "en"  # "pt" if you want Portuguese output
