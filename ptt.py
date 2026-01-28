# ptt.py
import sys
import time
from typing import Optional

class PTT:
    def __init__(self, key_name: str):
        self.key_name = key_name
        self._pressed = False
        self._backend = None

        if sys.platform.startswith("win"):
            try:
                import keyboard  # type: ignore
                self._backend = ("keyboard", keyboard)
            except ImportError:
                self._backend = None
        else:
            try:
                from pynput import keyboard as pkb  # type: ignore
                self._backend = ("pynput", pkb)
                self._listener = pkb.Listener(
                    on_press=self._on_press,
                    on_release=self._on_release
                )
                self._listener.start()
            except ImportError:
                self._backend = None

    def available(self) -> bool:
        return self._backend is not None

    def is_pressed(self) -> bool:
        if self._backend is None:
            return False
        name, mod = self._backend
        if name == "keyboard":
            # Windows only
            return mod.is_pressed(self.key_name)
        else:
            return self._pressed

    # pynput callbacks (macOS/Linux)
    def _on_press(self, key):
        if self._matches(key):
            self._pressed = True

    def _on_release(self, key):
        if self._matches(key):
            self._pressed = False

    def _matches(self, key) -> bool:
        # Very simple mapping: supports ctrl/shift/alt/space/enter and single chars.
        try:
            from pynput.keyboard import Key  # type: ignore
            k = self.key_name.lower().strip()
            if k in ("right ctrl", "ctrl_r"):
                return key == Key.ctrl_r
            if k in ("left ctrl", "ctrl_l"):
                return key == Key.ctrl_l
            if k in ("space",):
                return key == Key.space
            if k in ("enter", "return"):
                return key == Key.enter
            if hasattr(key, "char") and key.char:
                return key.char.lower() == k
        except Exception:
            pass
        return False
