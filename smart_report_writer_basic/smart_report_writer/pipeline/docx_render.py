from __future__ import annotations
from typing import Dict
try:
    from docxtpl import DocxTemplate, RichText
except Exception:
    DocxTemplate = None
    RichText = None

def ctx_map(ctx) -> Dict[str,str]:
    src = "\n".join(f"- {d.path} ({d.mimetype or 'unknown'})" for d in ctx.docs)
    return {
        "TOPIC": (ctx.topic or "").strip(),
        "EXEC_SUMMARY": (ctx.llm_sections.get("summary_text") or "").strip(),
        "DOCS": (ctx.llm_sections.get("docs_text") or "").strip(),
        "TABLES": (ctx.llm_sections.get("tables_text") or "").strip(),
        "LOGS": (ctx.llm_sections.get("logs_text") or "").strip(),
        "CODE": (ctx.llm_sections.get("code_text") or "").strip(),
        "SOURCES": src.strip(),
    }

def docx_fill(template_path: str, mapping: Dict[str,str], out_path: str) -> str:
    if DocxTemplate is None:
        raise RuntimeError("docxtpl required. pip install docxtpl")
    doc = DocxTemplate(template_path)
    rt = {}
    for k, v in mapping.items():
        if RichText:
            r = RichText()
            first = True
            for line in (v or "").splitlines():
                if not first:
                    r.add("\n")
                r.add(line)
                first = False
            rt[k] = r
        else:
            rt[k] = v or ""
    doc.render(rt)
    doc.save(out_path)
    return out_path
