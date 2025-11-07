from __future__ import annotations
try:
    from bs4 import BeautifulSoup  # optional
except Exception:
    BeautifulSoup = None

def extract_visible_text(path: str) -> str:
    if BeautifulSoup is None:
        # Fallback: just return raw file in case user wants some content
        try:
            with open(path, "rb") as f:
                return f.read().decode("utf-8", "ignore")
        except Exception:
            return ""
    try:
        with open(path, "rb") as f:
            data = f.read()
        soup = BeautifulSoup(data, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        return text
    except Exception as e:
        return f"[HTML parse error] {e}"
