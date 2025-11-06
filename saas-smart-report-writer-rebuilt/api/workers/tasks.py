import json, traceback
from celery import shared_task
from common.db import SessionLocal
from common.models import Job
from common.storage import put_object, s3_url_for
from common.srw_adapter import run_pipeline_to_artifacts

@shared_task(name="run_summarize_pipeline")
def run_summarize_pipeline(job_id: str):
    with SessionLocal() as db:
        job = db.get(Job, job_id)
        if not job:
            return
        try:
            job.status = "running"
            db.commit()

            artifacts = run_pipeline_to_artifacts(job.sources_list, template=job.template)
            uploaded = []
            for name, content, mime in artifacts:
                key = f"artifacts/{job.org_id}/{job.id}/{name}"
                put_object(key, content, mime_type=mime)
                uploaded.append(s3_url_for(key))

            job.status = "done"
            job.artifacts_list = uploaded
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.error = f"{e}\n{traceback.format_exc()}"
            db.commit()
            raise
