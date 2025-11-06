from pydantic import BaseModel, Field
from typing import List, Optional

class FileInitiateRequest(BaseModel):
    filename: str
    mime_type: str

class FileInitiateResponse(BaseModel):
    key: str
    upload_url: str

class FileCompleteRequest(BaseModel):
    key: str

class FileGetLinkResponse(BaseModel):
    key: str
    download_url: str

class JobCreateRequest(BaseModel):
    sources: List[str] = Field(default_factory=list)
    template: Optional[str] = None

class JobCreateResponse(BaseModel):
    job_id: str

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    artifacts: List[str] = Field(default_factory=list)
    error: Optional[str] = None
