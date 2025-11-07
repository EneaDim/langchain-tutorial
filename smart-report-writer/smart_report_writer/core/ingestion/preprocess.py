from pydantic import BaseModel
from smart_report_writer.core.utils.security import sniff_mime, sha256
from smart_report_writer.core.models.domain import ContentKind

class DetectedInfo(BaseModel):
    mime: str
    content_kind: ContentKind
    sha256: str
    extra: dict = {}

def detect_and_extract_metadata(data: bytes, filename: str, settings) -> DetectedInfo:
    mime = sniff_mime(data)
    kind = classify_mime(mime, filename.lower())
    return DetectedInfo(mime=mime, content_kind=kind, sha256=sha256(data), extra={})

def classify_mime(mime: str, filename: str) -> ContentKind:
    if any(ext in filename for ext in [".csv",".tsv",".xlsx",".xls",".json",".jsonl",".xml",".parquet"]):
        return ContentKind.tabular
    if any(ext in filename for ext in [".py",".js",".ts",".java",".c",".cpp",".go",".rs",".cs",".sql",".sh"]):
        return ContentKind.code
    if any(ext in filename for ext in [".zip",".tar",".tgz",".tar.gz"]):
        return ContentKind.archive
    if any(ext in filename for ext in [".eml",".mbox"]):
        return ContentKind.email
    if any(ext in filename for ext in [".png",".jpg",".jpeg",".tif",".tiff",".mp3",".wav",".flac"]):
        return ContentKind.media
    return ContentKind.document
