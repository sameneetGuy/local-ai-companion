import numpy as np
from piper.voice import PiperVoice

class PiperTTS:
    def __init__(self, model_path: str, config_path: str | None = None):
        try:
            if config_path is not None:
                self.voice = PiperVoice.load(model_path, config_path)
            else:
                self.voice = PiperVoice.load(model_path)
        except TypeError:
            self.voice = PiperVoice.load(model_path)

        self.sample_rate = int(self.voice.config.sample_rate)

    def synth(self, text: str, language: str = "en", speaker_wav: str | None = None):
        parts = []
        sr = self.sample_rate

        for chunk in self.voice.synthesize(text):
            a16 = chunk.audio_int16_array
            if a16 is None:
                continue
            parts.append(np.asarray(a16, dtype=np.int16))
            if chunk.sample_rate:
                sr = int(chunk.sample_rate)

        if not parts:
            return np.zeros((0,), dtype=np.float32), int(sr)

        pcm16 = np.concatenate(parts)
        audio = pcm16.astype(np.float32) / 32768.0
        return audio, int(sr)
