from __future__ import annotations
import os, re, csv, json
from typing import Optional, Any, Dict, List
import pandas as pd

try:
    import chardet  # optional
except Exception:
    chardet = None

from .html_soup import extract_visible_text as _html_to_text
from .pdf import pdf_text as _pdf_text
from .docx_text import docx_text as _docx_text
from .excel import load_excel_sheets
from .tables import load_table_like, profile_df

class LoadedDoc:
    def __init__(self, path: str, mimetype: Optional[str], text: str, tables: Optional[list[pd.DataFrame]] = None):
        self.path = path
        self.mimetype = mimetype
        self.text = text or ""
        self.tables = tables or []

def detect_encoding(data: bytes) -> str:
    if chardet is None:
        return "utf-8"
    try:
        res = chardet.detect(data)
        return res.get("encoding") or "utf-8"
    except Exception:
        return "utf-8"

def readb(p: str) -> bytes:
    with open(p, "rb") as f:
        return f.read()

def ensure_dir(p: str):
    if p and not os.path.exists(p):
        os.makedirs(p, exist_ok=True)

def safe_path(p: str) -> str:
    if not os.path.exists(p):
        return p
    r, e = os.path.splitext(p)
    i = 0
    while True:
        c = f"{r}_{i}{e}"
        if not os.path.exists(c):
            return c
        i += 1

def norm_text(t: str, cap: int) -> str:
    if not t:
        return ""
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = re.sub(r"\n{3,}", "\n\n", t)
    return t[:cap] if cap > 0 else t

def _load_textlike(path: str, data: bytes) -> str:
    enc = detect_encoding(data)
    try:
        return data.decode(enc, "ignore")
    except Exception:
        return ""

def load_any(path: str) -> LoadedDoc:
    ext = os.path.splitext(path)[1].lower()
    try:
        data = readb(path)
    except Exception:
        data = b""

    try:
        if ext in [".csv", ".tsv"]:
            df = load_table_like(path)
            return LoadedDoc(path, "text/csv", f"CSV/TSV {df.shape}", [df])

        if ext in [".xlsx", ".xls"]:
            tabs = load_excel_sheets(path)
            return LoadedDoc(path, "application/vnd.ms-excel", f"Excel sheets: {len(tabs)}", tabs)

        if ext == ".json":
            enc = detect_encoding(data)
            obj = json.loads(data.decode(enc, "ignore"))
            if isinstance(obj, list):
                try:
                    df = pd.json_normalize(obj)
                    return LoadedDoc(path, "application/json", "JSON list", [df])
                except Exception:
                    pass
            if isinstance(obj, dict):
                for k in ["data", "rows", "items", "records", "results"]:
                    if k in obj and isinstance(obj[k], list):
                        try:
                            df = pd.json_normalize(obj[k])
                            return LoadedDoc(path, "application/json", f"JSON dict[{k}]", [df])
                        except Exception:
                            pass
            return LoadedDoc(path, "application/json", json.dumps(obj, ensure_ascii=False, indent=2), [])

        if ext == ".pdf":
            return LoadedDoc(path, "application/pdf", _pdf_text(path), [])

        if ext == ".docx":
            return LoadedDoc(path, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", _docx_text(path), [])

        if ext in [".html", ".htm"]:
            return LoadedDoc(path, "text/html", _html_to_text(path), [])

        if ext in [".md", ".txt", ".log", ".ini", ".cfg", ".conf", ".yaml", ".yml"]:
            return LoadedDoc(path, "text/plain", _load_textlike(path, data), [])

    except Exception as e:
        return LoadedDoc(path, None, f"[Loader error] {e}", [])

    # fallback: try decode
    enc = detect_encoding(data)
    try:
        return LoadedDoc(path, None, data.decode(enc, "ignore"), [])
    except Exception:
        return LoadedDoc(path, None, "[Unsupported format]", [])

def kind_for(path: str) -> str:
    p = path.lower()
    if any(p.endswith(x) for x in [".py", ".js", ".ts", ".java", ".go", ".rb", ".rs", ".cs", ".cpp", ".hpp", ".c", ".h", ".ipynb"]):
        return "code"
    if any(p.endswith(x) for x in [".log", ".ini", ".cfg", ".conf", ".yaml", ".yml"]):
        return "logcfg"
    if any(p.endswith(x) for x in [".csv", ".tsv", ".xlsx", ".xls", ".json"]):
        return "table"
    return "doc"
