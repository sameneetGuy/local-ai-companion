# llm_ollama.py
import requests

class OllamaChat:
    def __init__(self, url: str, model: str, system_prompt: str):
        self.url = url
        self.model = model
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": system_prompt}]

    def ask(self, user_text: str) -> str:
        self.history.append({"role": "user", "content": user_text})

        payload = {
            "model": self.model,
            "messages": self.history,
            "stream": False,
        }
        r = requests.post(self.url, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()

        answer = data["message"]["content"].strip()
        self.history.append({"role": "assistant", "content": answer})
        return answer
