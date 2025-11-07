def enforce_limits(text: str, max_chars: int = 20000) -> str:
    return text[:max_chars]
