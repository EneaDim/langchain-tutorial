from __future__ import annotations
try:
    import docx as py_docx  # optional
except Exception:
    py_docx = None

def docx_text(path: str) -> str:
    if py_docx is None:
        return "[Install python-docx]"
    try:
        d = py_docx.Document(path)
        texts = [p.text for p in d.paragraphs if p.text and p.text.strip()]
        return "\n".join(texts)
    except Exception as e:
        return f"[DOCX error] {e}"
