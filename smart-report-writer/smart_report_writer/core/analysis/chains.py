import json
from .prompts import DOC_PROMPT, TABULAR_PROMPT, CODE_PROMPT
from .llama_ollama import OllamaClient
from .qwen_ollama import OllamaClient as QwenOllamaClient
from .openai import run_openai
from .vllm import run_vllm

def repair_json(s: str) -> dict:
    try:
        return json.loads(s)
    except Exception:
        s2 = s[s.find("{"):s.rfind("}")+1]
        return json.loads(s2)

def run_chain(kind: str, content: dict, provider: str, model: str, settings) -> dict:
    if kind == "document":
        prompt = DOC_PROMPT + "\n\n" + content["text"][:8000]
    elif kind == "tabular":
        prompt = TABULAR_PROMPT + "\n\n" + json.dumps(content["profile"])[:8000]
    elif kind == "code":
        prompt = CODE_PROMPT + "\n\n" + content["preview"][:8000]
    else:
        prompt = "Return JSON {}"

    if provider == "LLAMA_OLLAMA":
        client = OllamaClient(settings.ollama_base_url)
        out = client.chat(model=model, messages=[{"role":"user","content":prompt}])
    elif provider == "QWEN_OLLAMA":
        client = QwenOllamaClient(settings.ollama_base_url)
        out = client.chat(model=model, messages=[{"role":"user","content":prompt}])
    elif provider == "OPENAI":
        out = run_openai(prompt, model, settings.openai_api_key, settings.openai_base_url or None)
    elif provider == "VLLM":
        out = run_vllm(prompt, settings.vllm_endpoint, model)
    else:
        raise ValueError("Unsupported provider")

    return repair_json(out)
