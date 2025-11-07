from fastapi import APIRouter, Depends
from .deps import get_settings
from smart_report_writer.core.models.responses import JobStatusResponse, DownloadLinkResponse
from worker.adapters import job_store

router = APIRouter(prefix="/v1/jobs", tags=["jobs"])

@router.get("/{job_id}", response_model=JobStatusResponse)
def status(job_id: str, settings=Depends(get_settings)):
    j = job_store.get(job_id)
    if not j:
        return JobStatusResponse(job_id=job_id, status="unknown", message="No such job")
    return JobStatusResponse(**j)

@router.get("/{job_id}/artifact", response_model=DownloadLinkResponse)
def artifact(job_id: str, settings=Depends(get_settings)):
    j = job_store.get(job_id)
    if not j or "artifact_url" not in j:
        return DownloadLinkResponse(url=None)
    return DownloadLinkResponse(url=j["artifact_url"])
