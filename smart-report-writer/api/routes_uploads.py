from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from smart_report_writer.core.ingestion import preprocess
from smart_report_writer.core.ingestion.repository import DocumentRepository
from smart_report_writer.core.models.requests import UploadRequest
from smart_report_writer.core.models.responses import DownloadLinkResponse
from smart_report_writer.core.models.domain import ContentKind, Document
from smart_report_writer.core.ingestion.validators import validate_file
from .deps import get_db_session, get_storage, get_settings
from sqlalchemy.orm import Session

router = APIRouter(prefix="/v1/uploads", tags=["uploads"])

@router.post("", response_model=dict)
async def upload(file: UploadFile = File(...),
                 req: UploadRequest = Depends(),
                 db: Session = Depends(get_db_session),
                 storage=Depends(get_storage),
                 settings=Depends(get_settings)):
    raw = await file.read()
    validate_file(raw, file.filename, max_mb=settings.max_upload_mb)
    info = preprocess.detect_and_extract_metadata(raw, file.filename, settings=settings)

    repo = DocumentRepository(db)
    doc = repo.create_document(
        filename=file.filename,
        mime=info.mime,
        content_kind=info.content_kind,
        size_bytes=len(raw),
        sha256=info.sha256,
        extra=info.extra,
    )
    key = storage.put_bytes(raw, key=f"uploads/{doc.id}/{file.filename}")
    url = storage.get_presigned_url(key)
    return {"data": {"document_id": str(doc.id), "content_kind": info.content_kind.value, "signed_url": url},
            "error": None, "meta": {}}
