from typing import Dict, Any
from pathlib import Path
import yaml
from smart_report_writer.core.generation.renderer import render
from smart_report_writer.core.generation.exporters import to_html, to_pdf
from smart_report_writer.core.analysis.chains import run_chain
from smart_report_writer.core.ingestion.documents import to_chunks, extract_text_from_pdf, extract_text_from_docx, extract_text_from_html, extract_text_from_md
from smart_report_writer.core.ingestion.tabular import load_table, profile_dataframe
from smart_report_writer.core.ingestion.code import detect_language, chunk_code
from smart_report_writer.core.models.settings import AppSettings

def generate_report_pipeline(req, repo, storage, settings: AppSettings):
    # Load document metadata/content
    # For brevity we assume object in S3 at "uploads/<doc_id>/<filename>" and re-ingest as needed.

    # Determine template metadata
    templates_cfg = yaml.safe_load((Path("config/templates.yml")).read_text())
    template_id = req.template_id
    meta = next((t for t in templates_cfg if t["id"] == template_id), None)
    if not meta:
        raise ValueError("Unknown template_id")

    # Load Jinja
    template_path = Path(f"smart_report_writer/core/templates/{meta['file']}")
    template_str = template_path.read_text()

    # Simulated content input for demo; in production you'd fetch bytes from storage and dispatch
    content_kind = meta["content_kind"]
    analysis_input: Dict[str, Any] = {}

    if content_kind == "document":
        sample = "This is a placeholder content to demonstrate pipeline end-to-end."
        chunks = to_chunks(sample)
        analysis_input = {"text": sample, "chunks": chunks}
    elif content_kind == "tabular":
        import pandas as pd
        df = pd.DataFrame({"country":["CH","DE","FR"], "gdp":[824,4200,2900]})
        profile = profile_dataframe(df)
        analysis_input = {"profile": profile}
    elif content_kind == "code":
        code = "def foo():\n    return 42\nclass Bar:\n    pass"
        lang = detect_language(code, filename="sample.py")
        chunks = chunk_code(code)
        analysis_input = {"preview": code, "language": lang, "chunks": chunks}
    else:
        raise ValueError("Unsupported content kind for demo")

    overrides = req.overrides.model_dump() if req.overrides else {
        "provider": settings.provider_default,
        "model": settings.model_default,
        "temperature": 0.1,
        "top_p": 1.0,
        "max_tokens": 1024,
    }

    analysis = run_chain(content_kind, analysis_input, provider=overrides["provider"], model=overrides["model"], settings=settings)

    context = {"analysis": analysis, "meta": meta, "input": analysis_input}
    html = render(template_str, context)
    artifact_bytes = to_html(html) if meta.get("export","html") == "html" else to_pdf(html)
    key = f"artifacts/{req.document_id}/{template_id}.{'html' if meta.get('export','html')=='html' else 'pdf'}"
    storage.put_bytes(artifact_bytes, key)
    url = storage.get_presigned_url(key)

    class Result: pass
    r = Result()
    r.download_url = url
    return r
