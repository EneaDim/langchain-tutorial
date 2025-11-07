from typing import Dict, Any
from PIL import Image
import io, pytesseract

def ocr_image(data: bytes) -> str:
    img = Image.open(io.BytesIO(data))
    return pytesseract.image_to_string(img)

def stt_audio(data: bytes, fmt: str = "wav") -> str:
    # For brevity, pretend we decode via whisper-timestamped (requires ffmpeg)
    return "[transcript placeholder]"  # can be swapped with real call if enabled
