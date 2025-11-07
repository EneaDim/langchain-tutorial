import httpx

def run_vllm(prompt: str, endpoint: str, model: str) -> str:
    r = httpx.post(f"{endpoint.rstrip('/')}/generate", json={"model": model, "prompt": prompt, "temperature":0.1})
    r.raise_for_status()
    return r.json().get("text","")
