from fastapi import APIRouter, Depends, HTTPException
from common.auth import require_auth
from common.schemas import JobCreateRequest, JobCreateResponse, JobStatusResponse
from common.db import SessionLocal
from common.models import Job
from api.workers.tasks import run_summarize_pipeline

router = APIRouter()

@router.post("", response_model=JobCreateResponse)
def create_job(req: JobCreateRequest, user=Depends(require_auth)):
    if not req.sources:
        raise HTTPException(400, "No sources provided")
    with SessionLocal() as db:
        job = Job.new(user.org_id, req.sources, req.template)
        db.add(job)
        db.commit()
        db.refresh(job)
        run_summarize_pipeline.delay(str(job.id))
        return JobCreateResponse(job_id=str(job.id))

@router.get("/{job_id}", response_model=JobStatusResponse)
def get_job(job_id: str, user=Depends(require_auth)):
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        if not job or job.org_id != user.org_id:
            raise HTTPException(404, "Not found")
        return JobStatusResponse(
            job_id=str(job.id),
            status=job.status,
            artifacts=job.artifacts_list if job.artifacts else [],
            error=job.error,
        )
