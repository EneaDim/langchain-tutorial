from smart_report_writer.core.utils.security import assert_size, assert_safe_filename
from common.exceptions import ValidationError

def validate_file(data: bytes, filename: str, max_mb: int = 200):
    assert_safe_filename(filename)
    assert_size(data, max_mb)
    if len(data) == 0:
        raise ValidationError("Empty file")
