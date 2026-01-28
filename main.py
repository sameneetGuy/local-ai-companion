# main.py
import os, inspect
import time
import numpy as np
import sounddevice as sd

from config import Config
from audio_io import AudioStream, bytes_to_int16
from vad import VADRecorder
from asr import ASR
from llm_ollama import OllamaChat
from tts_piper import PiperTTS

from openwakeword.model import Model as OWWModel
from openwakeword.utils import download_models

def iter_audio_frames(stream: AudioStream):
    while True:
        yield stream.read()

def play_audio(wav: np.ndarray, sr: int):
    sd.play(wav, sr)
    sd.wait()

def main():
    cfg = Config()

    # ----- Audio capture -----
    blocksize = int(cfg.sample_rate * (cfg.block_ms / 1000.0))
    stream = AudioStream(
        samplerate=cfg.sample_rate,
        blocksize=blocksize,
        device=cfg.input_device,
        channels=cfg.channels,
    )
    stream.start()
    audio_iter = iter_audio_frames(stream)

    # ----- Wake word -----
    # Ensure models are present (downloads once)
    download_models()

    # Force ONNX runtime backend by selecting ONNX models explicitly
    oww_root = os.path.dirname(inspect.getfile(openwakeword))
    
    oww = OWWModel(
        wakeword_models=[
            os.path.join(oww_root, "resources", "models", "hey_jarvis_v0.1.onnx"),
        ]
    )
    consecutive = 0
    last_trigger_t = 0.0

    # ----- VAD recorder -----
    vadrec = VADRecorder(
        sample_rate=cfg.sample_rate,
        frame_ms=cfg.block_ms,
        aggressiveness=cfg.vad_aggressiveness,
        min_speech_ms=cfg.min_speech_ms,
        end_silence_ms=cfg.end_silence_ms,
        max_record_s=cfg.max_record_s,
    )

    # ----- PTT -----
    ptt = PTT(cfg.ptt_key)
    if not ptt.available():
        print("PTT backend not available on this system (PTT disabled).")
    
    # ----- ASR / LLM / TTS -----
    asr = ASR(cfg.whisper_model, cfg.whisper_device, cfg.whisper_compute_type)
    llm = OllamaChat(cfg.ollama_url, cfg.ollama_model, cfg.system_prompt)
    voice = cfg.piper_voices[cfg.tts_voice]
    tts = PiperTTS(voice["model"], voice["config"])

    print("=== Local AI Companion (PC) ===")
    print(f"- Wake word: OpenWakeWord (threshold={cfg.wakeword_threshold})")
    print(f"- PTT key: hold [{cfg.ptt_key}] (may need admin)")
    print("Make sure Ollama is running and the model is pulled:")
    print(f"  ollama run {cfg.ollama_model}")
    print("--------------------------------")

    def run_one_turn(reason: str):
        print(f"\n[{reason}] Listening...")
        utter = vadrec.record_utterance(audio_iter)
        if utter is None:
            print("No speech detected.")
            return

        pcm16 = bytes_to_int16(utter)
        text = asr.transcribe_int16(pcm16, sample_rate=cfg.sample_rate)
        if not text:
            print("ASR produced empty text.")
            return

        print(f"You: {text}")
        answer = llm.ask(text)
        print(f"AI: {answer}")

        wav, sr = tts.synth(answer, language=cfg.tts_language, speaker_wav=cfg.speaker_wav)
        play_audio(wav, sr)

    try:
        while True:
            # --- PTT (Option C fallback) ---
            if ptt.is_pressed():
                # simple debounce
                time.sleep(0.05)
                run_one_turn("PTT")
                # wait until released to avoid retrigger loop
                while ptt.is_pressed():
                    time.sleep(0.05)
                continue

            # --- Wake word loop (cheap always-on) ---
            now = time.time()
            if now - last_trigger_t < cfg.wakeword_cooldown_s:
                # Still cooling down
                _ = next(audio_iter)
                continue

            frame = next(audio_iter)  # raw int16 bytes for cfg.block_ms
            audio_i16 = np.frombuffer(frame, dtype=np.int16)

            preds = oww.predict(audio_i16)
            # preds is dict of wakeword -> confidence
            best_word, best_score = None, 0.0
            for k, v in preds.items():
                if v > best_score:
                    best_word, best_score = k, v

            if best_score >= cfg.wakeword_threshold:
                consecutive += 1
            else:
                consecutive = 0

            if consecutive >= cfg.wakeword_consecutive_hits:
                last_trigger_t = time.time()
                consecutive = 0
                print(f"\n[WakeWord] Detected: {best_word} ({best_score:.2f})")
                run_one_turn("WakeWord")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        stream.stop()

if __name__ == "__main__":
    main()
