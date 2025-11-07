from __future__ import annotations
import os
from typing import Dict, List, Any
import pandas as pd
from ..loaders.files import norm_text
from ..loaders.files import LoadedDoc as LoaderDoc
from .types import LoadedDoc

def convert_loaderdoc(d: LoaderDoc) -> LoadedDoc:
    return LoadedDoc(path=d.path, mimetype=d.mimetype, text=d.text, tables=d.tables)

def bucket_docs(loaded_docs: list[LoaderDoc]) -> dict[str, list[LoadedDoc]]:
    # assumes caller already decided kinds; we just wrap
    buckets = {"doc": [], "logcfg": [], "table": [], "code": []}
    return buckets

def cap_and_combine(docs: list[LoadedDoc], per_file_cap: int, total_cap: int) -> str:
    combined: list[str] = []
    tot = 0
    for d in docs:
        if not d.text.strip():
            continue
        ch = norm_text(d.text, per_file_cap)
        if total_cap > 0 and tot + len(ch) > total_cap:
            rem = max(0, total_cap - tot)
            if rem > 0:
                combined.append(ch[:rem] + "\n...[truncated]...")
            break
        combined.append(ch)
        tot += len(ch)
    return "\n\n".join(combined)
