import requests
from ..config import settings

def chat(prompt: str) -> str:
    url = f"{settings.ollama_base_url}/api/generate"
    data = {"model": settings.ollama_model, "prompt": prompt, "stream": False}
    r = requests.post(url, json=data, timeout=300)
    r.raise_for_status()
    return r.json().get("response", "")
