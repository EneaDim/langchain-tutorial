import httpx
from typing import Dict, Any

class OllamaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def chat(self, model: str, messages: list[Dict[str,str]], temperature: float = 0.1, max_tokens: int = 2048) -> str:
        payload = {"model": model, "messages": messages, "options": {"temperature": temperature, "num_predict": max_tokens}}
        r = httpx.post(f"{self.base_url}/v1/chat/completions", json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        return data["choices"][0]["message"]["content"]
