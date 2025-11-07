import hashlib, magic, os
from common.exceptions import ValidationError

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sniff_mime(data: bytes) -> str:
    return magic.from_buffer(data, mime=True) or "application/octet-stream"

def assert_safe_filename(name: str):
    if "/" in name or "\\" in name or name.startswith("."):
        raise ValidationError("Unsafe filename")

def assert_size(data: bytes, max_mb: int):
    if len(data) > max_mb * 1024 * 1024:
        raise ValidationError(f"File exceeds {max_mb} MB")
