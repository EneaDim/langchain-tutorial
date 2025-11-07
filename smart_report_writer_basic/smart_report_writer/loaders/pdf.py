from __future__ import annotations
try:
    import pdfplumber  # optional
except Exception:
    pdfplumber = None

def pdf_text(path: str) -> str:
    if pdfplumber is None:
        return "[Install pdfplumber]"
    texts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                try:
                    t = page.extract_text() or ""
                    if t.strip():
                        texts.append(t)
                except Exception:
                    pass
        return "\n\n".join(texts)
    except Exception as e:
        return f"[PDF error] {e}"
