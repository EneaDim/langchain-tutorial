from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from .llm import LLMConfig

class UploadRequest(BaseModel):
    antivirus: bool = False

class GenerateRequest(BaseModel):
    document_id: str
    template_id: str
    overrides: Optional[LLMConfig] = None
    idempotency_key: Optional[str] = Field(default=None)
