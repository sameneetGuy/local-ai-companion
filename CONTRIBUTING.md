# Contributing

Thanks for your interest in contributing to **Local AI Companion**! 🎉

This project is intentionally modular and hackable. Contributions of all sizes are welcome.

---

## Ways to contribute

You can help by:
- Fixing bugs or edge cases
- Improving documentation
- Adding cross-platform compatibility fixes
- Improving ASR / TTS / wake word reliability
- Proposing new features (skills, UI layers, plugins, etc.)

If you’re unsure where to start, opening an issue to discuss ideas is always welcome.

---

## Development setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Make your changes in a feature branch

---

## Code style & structure
- Keep modules small and focused
- Prefer explicit logic over clever tricks
- Avoid hard-coding OS-specific behavior
- New functionality should be configurable via config.py when applicable
This project favors clarity and modularity over premature optimization.

---

## Platform considerations
This project targets:
- Windows
- macOS
- Linux
Please avoid introducing changes that break cross-platform compatibility unless clearly documented.

Audio and hotkey behavior may differ by OS — graceful degradation is preferred over hard failure.

---

## Licensing
By contributing to this repository, you agree that your contributions will be licensed under the MIT License, consistent with the rest of the project.

You should not submit code or assets that are incompatible with MIT or that impose additional licensing restrictions.

---

## Questions?
If you’re unsure about anything, feel free to open an issue and ask.