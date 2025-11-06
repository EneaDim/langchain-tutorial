import uuid, json, os, tempfile, shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from common.auth import require_auth
from common.schemas import JobCreateRequest, JobStatusResponse
from common.storage import presign_get, put_bytes
from common.config import settings
from common import srw_adapter

# For the skeleton, keep job state in a simple dict (replace with DB in production)
JOBS: dict[str, dict] = {}

router = APIRouter()

@router.post("", response_model=JobStatusResponse)
def create_job(req: JobCreateRequest, user=Depends(require_auth)):
    job_id = str(uuid.uuid4())
    # In production: resolve file_ids -> S3 keys and download locally first.
    # Here, we simulate by requiring the client to upload local paths as file_ids that are already accessible.
    JOBS[job_id] = {"status": "running", "artifacts": None, "error": None}
    try:
        with tempfile.TemporaryDirectory() as td:
            # Expect req.file_ids to be absolute/local paths for the skeleton run
            outputs = srw_adapter.run_summary(
                local_files=req.file_ids,
                topic=req.topic,
                model=req.model or settings.ollama_model,
                temperature=req.temperature or settings.model_temperature,
                per_file_cap=req.per_file_cap or settings.srw_per_file_cap,
                total_cap=req.total_cap or settings.srw_total_cap,
                template_path=None,  # template handling omitted in skeleton
            )
            # Upload artifacts to S3 and return signed URLs
            arts = {}
            for k, path in outputs.items():
                key = f"artifacts/{job_id}/{os.path.basename(path)}"
                with open(path, "rb") as f:
                    put_bytes(key, f.read(), "text/markdown" if path.endswith(".md") else "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                arts[k] = presign_get(key)
            JOBS[job_id]["status"] = "done"
            JOBS[job_id]["artifacts"] = arts
    except Exception as e:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error"] = str(e)
    return JobStatusResponse(id=job_id, status=JOBS[job_id]["status"], artifacts=JOBS[job_id]["artifacts"], error=JOBS[job_id]["error"])

@router.get("/{job_id}", response_model=JobStatusResponse)
def job_status(job_id: str, user=Depends(require_auth)):
    j = JOBS.get(job_id)
    if not j:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(id=job_id, status=j["status"], artifacts=j.get("artifacts"), error=j.get("error"))
