import uuid
import os
from fastapi import APIRouter, Depends, HTTPException
from common.auth import require_auth
from common.storage import presign_put, presign_get
from common.schemas import FileInitiateRequest, FileInitiateResponse, FileCompleteRequest, FileGetLinkResponse

router = APIRouter()

@router.post("/initiate", response_model=FileInitiateResponse)
def initiate_upload(req: FileInitiateRequest, user=Depends(require_auth)):
    mime = (req.mime_type or 'application/octet-stream').split(';')[0].strip().lower()
env_allowed = [m.strip().lower() for m in os.getenv('ALLOWED_MIME_LIST','').split(',') if m.strip()]
user_allowed = []
try:
    user_allowed = [m.strip().lower() for m in (user.allowed_mime or [])]
except Exception:
    pass
allowed = set(env_allowed + user_allowed + ['application/octet-stream'])
if mime not in allowed:
    raise HTTPException(status_code=400, detail='mime not allowed')

    key = f"uploads/{user.org_id}/{uuid.uuid4()}/{req.filename}"
    url = presign_put(key=key, mime=req.mime_type)
    return FileInitiateResponse(key=key, upload_url=url)

@router.post("/complete")
def complete_upload(req: FileCompleteRequest, user=Depends(require_auth)):
    return {"status":"ok","key":req.key}

@router.get("/link", response_model=FileGetLinkResponse)
def get_link(key: str, user=Depends(require_auth)):
    return FileGetLinkResponse(key=key, download_url=presign_get(key))
