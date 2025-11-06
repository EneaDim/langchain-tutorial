import os, json, tempfile, subprocess, shutil, sys
from typing import List, Optional, Dict

SRW_PATH = "/opt/srw"  # mounted in dev

def _import_srw():
    if SRW_PATH not in sys.path and os.path.isdir(SRW_PATH):
        sys.path.insert(0, SRW_PATH)
    from smart_report_writer.cli import run_pipeline  # raises if not available
    return run_pipeline

def _try_module_run(local_files, topic, model, temperature, per_file_cap, total_cap, template_path) -> Dict[str, str]:
    run_pipeline = _import_srw()
    class _Args:
        def __init__(self):
            self.inputs = local_files
            self.recursive = False
            self.topic = topic
            self.summary_out = "summary.md"
            self.detailed_out = "report.md"
            self.model = model or os.environ.get("OLLAMA_MODEL","llama3.2:latest")
            self.base_url = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
            self.temperature = float(temperature if temperature is not None else os.environ.get("MODEL_TEMPERATURE","0.2"))
            self.per_file_cap = int(per_file_cap or int(os.environ.get("SRW_PER_FILE_CAP","12000")))
            self.total_cap = int(total_cap or int(os.environ.get("SRW_TOTAL_CAP","150000")))
            self.docx_template_file = template_path
    with tempfile.TemporaryDirectory() as td:
        cwd = os.getcwd()
        os.chdir(td)
        args = _Args()
        paths = run_pipeline(args)  # {"summary":..., "detailed":...}
        os.chdir(cwd)
        out = {"summary_path": paths["summary"], "detailed_path": paths["detailed"]}
        if out["detailed_path"].lower().endswith(".docx"):
            out["docx_path"] = out["detailed_path"]
        return out

def _run_cli(local_files, topic, model, temperature, per_file_cap, total_cap, template_path) -> Dict[str,str]:
    python = shutil.which("python") or "python"
    with tempfile.TemporaryDirectory() as td:
        summary_out = os.path.join(td, "summary.md")
        detailed_out = os.path.join(td, "report.md")
        args = [
            python, "-m", "smart_report_writer.cli",
            "-i", *local_files,
            "--topic", topic or "",
            "--summary-out", summary_out,
            "--detailed-out", detailed_out,
            "--model", model or os.environ.get("OLLAMA_MODEL","llama3.2:latest"),
            "--temperature", str(temperature if temperature is not None else os.environ.get("MODEL_TEMPERATURE","0.2")),
        ]
        if per_file_cap: args += ["--per-file-cap", str(per_file_cap)]
        if total_cap: args += ["--total-cap", str(total_cap)]
        if template_path: args += ["--docx-template-file", template_path]
        env = os.environ.copy()
        if SRW_PATH:
            # allow python -m to find the module without packaging
            env["PYTHONPATH"] = f"{SRW_PATH}:" + env.get("PYTHONPATH","")
        subprocess.run(args, check=True, env=env)
        out = {"summary_path": summary_out, "detailed_path": detailed_out}
        if template_path:
            docx_out = detailed_out if detailed_out.lower().endswith(".docx") else detailed_out.replace(".md",".docx")
            out["docx_path"] = docx_out
        return out

def run_summary(local_files: List[str], topic: Optional[str], model: Optional[str], temperature: Optional[float],
                per_file_cap: Optional[int], total_cap: Optional[int], template_path: Optional[str]) -> Dict[str,str]:
    try:
        return _try_module_run(local_files, topic, model, temperature, per_file_cap, total_cap, template_path)
    except Exception:
        return _run_cli(local_files, topic, model, temperature, per_file_cap, total_cap, template_path)
