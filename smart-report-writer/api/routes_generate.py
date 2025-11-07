from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .deps import get_db_session, get_settings
from smart_report_writer.core.models.requests import GenerateRequest
from smart_report_writer.core.models.responses import JobStatusResponse
from worker.tasks import enqueue_generate

router = APIRouter(prefix="/v1/generate", tags=["generate"])

@router.post("", response_model=JobStatusResponse)
def generate(req: GenerateRequest, db: Session = Depends(get_db_session), settings=Depends(get_settings)):
    job_id = enqueue_generate(req, settings=settings)
    return JobStatusResponse(job_id=job_id, status="queued", message="Job enqueued")
