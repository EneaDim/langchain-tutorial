from .celery_app import celery
# Placeholder: convert API /jobs endpoints to dispatch Celery tasks for real async processing.

@celery.task
def run_job(job_id: str):
    return {"job_id": job_id, "status": "done"}
