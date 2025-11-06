import os
from dataclasses import dataclass

DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
DEFAULT_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_TEMPERATURE = float(os.environ.get("MODEL_TEMPERATURE", "0.2"))
DEF_PER_FILE_CAP = int(os.environ.get("SRW_PER_FILE_CAP", "12000"))
DEF_TOTAL_CAP = int(os.environ.get("SRW_TOTAL_CAP", "150000"))

@dataclass
class Settings:
    inputs: list[str]
    recursive: bool = False
    topic: str | None = None
    summary_out: str = "summary.md"
    detailed_out: str = "report.md"
    model: str = DEFAULT_MODEL
    base_url: str = DEFAULT_BASE_URL
    temperature: float = DEFAULT_TEMPERATURE
    per_file_cap: int = DEF_PER_FILE_CAP
    total_cap: int = DEF_TOTAL_CAP
    docx_template_file: str | None = None
    stream: bool = False
