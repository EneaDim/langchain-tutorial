# Adapter placeholder for OpenAI-compatible endpoints
import os, requests
from ..config import settings

def chat(prompt: str) -> str:
    # Implement against /v1/chat/completions or /v1/completions
    return "not-implemented"
