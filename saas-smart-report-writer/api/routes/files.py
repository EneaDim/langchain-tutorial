import uuid, json
from fastapi import APIRouter, Depends, HTTPException
from common.auth import require_auth
from common.storage import presign_put
from common.schemas import FileInitiateRequest, FileInitiateResponse, FileCompleteRequest

router = APIRouter()

@router.post("/initiate", response_model=FileInitiateResponse)
def initiate_upload(req: FileInitiateRequest, user=Depends(require_auth)):
    file_id = str(uuid.uuid4())
    ps = presign_put(file_id, req.mime)
    return FileInitiateResponse(file_id=file_id, upload_url=ps["url"])

@router.post("/complete")
def complete_upload(req: FileCompleteRequest, user=Depends(require_auth)):
    # In production: persist file metadata to DB (omitted in skeleton)
    return {"ok": True, "file_id": req.file_id, "size": req.size}
