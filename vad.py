# vad.py
import webrtcvad

class VADRecorder:
    def __init__(self, sample_rate: int, frame_ms: int, aggressiveness: int,
                 min_speech_ms: int, end_silence_ms: int, max_record_s: float):
        if frame_ms not in (10, 20, 30):
            raise ValueError("WebRTC VAD only supports frame_ms in {10,20,30}")
        self.sample_rate = sample_rate
        self.frame_ms = frame_ms
        self.vad = webrtcvad.Vad(aggressiveness)

        self.min_speech_frames = max(1, min_speech_ms // frame_ms)
        self.end_silence_frames = max(1, end_silence_ms // frame_ms)
        self.max_frames = int((max_record_s * 1000) // frame_ms)

    def record_utterance(self, audio_iter):
        """
        audio_iter yields raw int16 PCM bytes of exactly frame_ms duration.
        Returns full utterance bytes (int16 PCM) or None if no speech.
        """
        frames = []
        speech_started = False
        speech_frames = 0
        silence_after_speech = 0

        for i in range(self.max_frames):
            frame = next(audio_iter)
            is_speech = self.vad.is_speech(frame, self.sample_rate)

            frames.append(frame)

            if is_speech:
                speech_frames += 1
                silence_after_speech = 0
                if speech_frames >= self.min_speech_frames:
                    speech_started = True
            else:
                if speech_started:
                    silence_after_speech += 1
                    if silence_after_speech >= self.end_silence_frames:
                        break

        if not speech_started:
            return None

        return b"".join(frames)
