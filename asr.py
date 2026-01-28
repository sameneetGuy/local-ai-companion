# asr.py
import numpy as np
from faster_whisper import WhisperModel

class ASR:
    def __init__(self, model_name: str, device: str, compute_type: str):
        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe_int16(self, pcm16: np.ndarray, sample_rate: int = 16000) -> str:
        # Convert int16 PCM to float32 in [-1, 1]
        audio = pcm16.astype(np.float32) / 32768.0
        segments, info = self.model.transcribe(audio, language="en", vad_filter=True)
        text = "".join(seg.text for seg in segments).strip()
        return text
