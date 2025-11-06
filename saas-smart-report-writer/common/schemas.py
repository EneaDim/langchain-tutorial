from pydantic import BaseModel, Field
from typing import List, Optional

class FileInitiateRequest(BaseModel):
    filename: str
    mime: str

class FileInitiateResponse(BaseModel):
    file_id: str
    upload_url: str

class FileCompleteRequest(BaseModel):
    file_id: str
    size: int

class JobCreateRequest(BaseModel):
    file_ids: List[str]
    topic: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    per_file_cap: Optional[int] = None
    total_cap: Optional[int] = None
    template_id: Optional[str] = None

class JobStatusResponse(BaseModel):
    id: str
    status: str
    artifacts: Optional[dict] = None
    error: Optional[str] = None
