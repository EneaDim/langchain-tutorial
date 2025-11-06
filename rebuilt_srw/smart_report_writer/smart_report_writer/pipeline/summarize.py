from __future__ import annotations
import os, json, asyncio
from typing import Dict, Any, List
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential

from ..llm import make_llm, stream_in_terminal
from ..prompts import DOC_SUMMARY_PROMPT, LOGCFG_SUMMARY_PROMPT, CODE_SUMMARY_PROMPT, TABLE_SUMMARY_PROMPT
from .chains import category_runnable, tables_runnable, master_runnable, arun
from .types import LoadedDoc, SummaryContext
from ..loaders.tables import profile_df

async def summarize_category_async(llm, docs: list[LoadedDoc], prompt, per_cap: int, total_cap: int) -> str:
    parts = []
    tot = 0
    for d in docs:
        if not d.text.strip():
            continue
        chunk = f"### {os.path.basename(d.path)}\n{d.text[:per_cap]}"
        parts.append(chunk)
        tot += len(chunk)
        if 0 < total_cap < tot:
            parts.append("\n...[truncated]...")
            break
    content = "\n\n".join(parts) if parts else "[No content]"
    runnable = category_runnable(llm, prompt)
    return await arun(runnable, content=content)

async def summarize_tables_async(llm, profiles: list[dict]) -> str:
    if not profiles:
        return "No tabular data detected."
    out = []
    runnable = tables_runnable(llm)
    for prof in profiles:
        txt = await arun(runnable, profile_json=json.dumps(prof, ensure_ascii=False))
        title = prof.get("name") or "table"
        out.append(f"#### {title}\n{txt}")
    return "\n\n".join(out)

async def run_all(llm, buckets: dict[str, list[LoadedDoc]]) -> dict[str,str]:
    # Build profiles
    profiles: list[dict] = []
    for d in buckets.get("table", []):
        for i, t in enumerate(d.tables):
            profiles.append(profile_df(t, name=f"{os.path.basename(d.path)}:table{i+1}"))

    docs_text, logs_text, code_text, tables_text = await asyncio.gather(
        summarize_category_async(llm, buckets.get("doc", []), DOC_SUMMARY_PROMPT, 12000, 150000),
        summarize_category_async(llm, buckets.get("logcfg", []), LOGCFG_SUMMARY_PROMPT, 12000, 150000),
        summarize_category_async(llm, buckets.get("code", []), CODE_SUMMARY_PROMPT, 12000, 150000),
        summarize_tables_async(llm, profiles)
    )
    return {
        "docs_text": docs_text,
        "logs_text": logs_text,
        "code_text": code_text,
        "tables_text": tables_text,
    }

async def synthesize_master(llm, manifest: list[dict], per_type_markdown: str, stream: bool = False) -> str:
    runnable = master_runnable(llm)
    inputs = {
        "manifest_json": json.dumps(manifest, ensure_ascii=False),
        "per_type_summaries": per_type_markdown or "N/A",
    }
    if stream:
        return stream_in_terminal(runnable, inputs)
    return await arun(runnable, **inputs)
