# audio_io.py
import queue
import numpy as np
import sounddevice as sd

class AudioStream:
    """
    Captures mono 16kHz int16 audio blocks and yields them as bytes.
    """
    def __init__(self, samplerate: int, blocksize: int, device: str | None, channels: int = 1):
        self.samplerate = samplerate
        self.blocksize = blocksize
        self.device = device
        self.channels = channels
        self.q: queue.Queue[bytes] = queue.Queue()
        self.stream: sd.RawInputStream | None = None

    def _callback(self, indata, frames, time, status):
        if status:
            # Avoid spamming; you can print if debugging
            pass
        self.q.put(bytes(indata))

    def start(self):
        self.stream = sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=self.blocksize,
            device=self.device,
            channels=self.channels,
            dtype="int16",
            callback=self._callback,
        )
        self.stream.start()

    def read(self) -> bytes:
        return self.q.get()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

def bytes_to_int16(audio_bytes: bytes) -> np.ndarray:
    return np.frombuffer(audio_bytes, dtype=np.int16)
