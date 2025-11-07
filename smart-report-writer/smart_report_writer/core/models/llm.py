from enum import Enum
from pydantic import BaseModel, Field

class Provider(str, Enum):
    LLAMA_OLLAMA = "LLAMA_OLLAMA"
    QWEN_OLLAMA = "QWEN_OLLAMA"
    OPENAI = "OPENAI"
    VLLM = "VLLM"

class LLMConfig(BaseModel):
    provider: Provider = Provider.LLAMA_OLLAMA
    model: str = "llama3:8b-instruct"
    temperature: float = 0.1
    top_p: float = 1.0
    max_tokens: int = 2048
