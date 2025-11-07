from pygments.lexers import guess_lexer_for_text
from typing import List, Dict

def detect_language(text: str, filename: str | None = None) -> str:
    try:
        return guess_lexer_for_text(text, filename=filename or "").name
    except Exception:
        return "PlainText"

def chunk_code(text: str) -> List[Dict]:
    # naive function/class block splitting
    lines = text.splitlines()
    chunks = []
    buf = []
    for line in lines:
        buf.append(line)
        if line.strip().startswith(("def ","class ","function ","fn ","public ","private ","package ")):
            if len(buf) > 1:
                chunks.append({"text":"\n".join(buf[:-1])})
                buf = [buf[-1]]
    if buf:
        chunks.append({"text":"\n".join(buf)})
    return chunks or [{"text": text}]
