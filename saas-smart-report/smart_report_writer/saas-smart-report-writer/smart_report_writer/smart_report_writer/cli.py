from __future__ import annotations

import argparse, asyncio, glob, os, json
from typing import List, Dict, Any
from .config import Settings, DEFAULT_MODEL, DEFAULT_BASE_URL, DEFAULT_TEMPERATURE, DEF_PER_FILE_CAP, DEF_TOTAL_CAP
from .llm import make_llm
from .prompts import *
from .loaders.files import load_any, kind_for, safe_path, ensure_dir
from .pipeline.types import LoadedDoc, SummaryContext
from .pipeline.summarize import run_all, synthesize_master
from .output.writers import ensure_env, write_with_template
from .pipeline.docx_render import ctx_map, docx_fill
PKG_DIR = os.path.dirname(__file__)

def main():
    ap = argparse.ArgumentParser(description="Smart Report Writer (Ollama + LangChain, modular)")
    ap.add_argument("--inputs", "-i", nargs="+", required=True)
    ap.add_argument("--recursive", action="store_true")
    ap.add_argument("--topic", type=str, default=None)
    ap.add_argument("--summary-out", type=str, default="summary.md")
    ap.add_argument("--detailed-out", type=str, default="report.md")
    ap.add_argument("--model", type=str, default=DEFAULT_MODEL)
    ap.add_argument("--base-url", type=str, default=DEFAULT_BASE_URL)
    ap.add_argument("--temperature", type=float, default=DEFAULT_TEMPERATURE)
    ap.add_argument("--per-file-cap", type=int, default=DEF_PER_FILE_CAP)
    ap.add_argument("--total-cap", type=int, default=DEF_TOTAL_CAP)
    ap.add_argument("--docx-template-file", type=str, default=None, help="Path to .docx template (docxtpl placeholders).")
    ap.add_argument("--stream", action="store_true", help="Stream master synthesis to terminal.")
    args = ap.parse_args()

    settings = Settings(
        inputs=args.inputs,
        recursive=args.recursive,
        topic=args.topic,
        summary_out=args.summary_out,
        detailed_out=args.detailed_out,
        model=args.model,
        base_url=args.base_url,
        temperature=args.temperature,
        per_file_cap=args.per_file_cap,
        total_cap=args.total_cap,
        docx_template_file=args.docx_template_file,
        stream=args.stream,
    )

    # Expand globs
    files: list[str] = []
    for patt in settings.inputs:
        files.extend(glob.glob(patt, recursive=settings.recursive))
    files = sorted(set(files))
    if not files:
        raise SystemExit("No files found.")

    # Load documents
    loaded = [load_any(p) for p in files]

    # Kind bucket (simple inline for clarity)
    buckets: dict[str, list[LoadedDoc]] = {"doc": [], "logcfg": [], "table": [], "code": []}
    for d in loaded:
        kind = kind_for(d.path)
        buckets[kind].append(LoadedDoc(path=d.path, mimetype=d.mimetype, text=d.text, tables=d.tables))

    # LLM
    llm = make_llm(settings.model, settings.base_url, settings.temperature, streaming=settings.stream)

    # Summaries
    parts = asyncio.run(run_all(llm, buckets))

    # Manifest
    manifest = [
        {"path": d.path, "type": kind_for(d.path), "mimetype": d.mimetype, "tables": len(d.tables), "chars": len(d.text or "")}
        for d in loaded
    ]

    # Per-type markdown
    per_type = []
    if parts["docs_text"].strip() and parts["docs_text"].strip() != "[No content]":
        per_type.append("## Documents\n" + parts["docs_text"])
    if parts["logs_text"].strip() and parts["logs_text"].strip() != "[No content]":
        per_type.append("## Logs / Configs\n" + parts["logs_text"])
    if parts["code_text"].strip() and parts["code_text"].strip() != "[No content]":
        per_type.append("## Code\n" + parts["code_text"])
    if parts["tables_text"].strip() and parts["tables_text"].strip() != "No tabular data detected.":
        per_type.append("## Tables\n" + parts["tables_text"])

    master = asyncio.run(synthesize_master(llm, manifest, "\n\n".join(per_type) if per_type else "N/A", stream=settings.stream))

    ctx = SummaryContext(
        topic=settings.topic,
        docs=[LoadedDoc(path=d.path, mimetype=d.mimetype, text=d.text, tables=d.tables) for d in loaded],
        combined_text="",
        table_stats=[],
        llm_sections={
            "summary_text": master,
            "tables_text": parts["tables_text"],
            "docs_text": parts["docs_text"],
            "logs_text": parts["logs_text"],
            "code_text": parts["code_text"],
        },
    )

    # Write outputs
    templates_dir = os.path.join(PKG_DIR, "output", "templates")
    if not os.path.isdir(templates_dir):
        raise SystemExit(f"Template directory missing: {templates_dir}")
    env = ensure_env(templates_dir)
    summ_out = safe_path(settings.summary_out)
    write_with_template(env, "summary.md.j2", ctx.__dict__ | {"title": "Executive Summary"}, summ_out)  # uses inline template path

    det_out = safe_path(settings.detailed_out)
    if settings.docx_template_file:
        if not det_out.lower().endswith(".docx"):
            r, _ = os.path.splitext(det_out)
            det_out = r + ".docx"
        docx_fill(settings.docx_template_file, ctx_map(ctx), det_out)
    else:
        write_with_template(env, "detailed.md.j2", ctx.__dict__ | {"title": "Smart Report"}, det_out)

    print(f"✅ Summary:  {summ_out}")
    print(f"✅ Detailed: {det_out}")

if __name__ == "__main__":
    main()
