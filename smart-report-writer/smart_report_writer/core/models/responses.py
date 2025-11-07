from pydantic import BaseModel
from typing import Optional

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    message: Optional[str] = None

class DownloadLinkResponse(BaseModel):
    url: Optional[str] = None
