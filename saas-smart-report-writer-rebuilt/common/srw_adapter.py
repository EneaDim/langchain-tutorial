from common.config import settings

def run_pipeline_to_artifacts(sources: list[str], template: str | None):
    from smart_report_writer.smart_report_writer.pipeline.summarize import run_all, synthesize_master
    from smart_report_writer.smart_report_writer.loaders.files import load_any
    from smart_report_writer.smart_report_writer.output.writers import render_docx_if_template

    docs = [load_any(src) for src in sources]

    cap_per = settings.srw_per_file_cap
    cap_total = settings.srw_total_cap
    ctxs = run_all(docs, per_file_cap=cap_per, total_cap=cap_total, temperature=settings.srw_temperature)
    master = synthesize_master(ctxs)

    artifacts = []
    summary_md = master.get("summary_md","").encode()
    report_md  = master.get("report_md","").encode()
    artifacts.append(("summary.md", summary_md, "text/markdown"))
    artifacts.append(("report.md", report_md, "text/markdown"))

    if settings.feature_docx and template and template != "none":
        docx_bytes = render_docx_if_template(report_md.decode(), template_id=template)
        if docx_bytes:
            artifacts.append(("report.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"))

    return artifacts
