import os
from celery import Celery
from typing import Dict, Any
from worker.adapters import new_job_id, set_status
from smart_report_writer.core.models.requests import GenerateRequest
from smart_report_writer.core.models.settings import AppSettings
from smart_report_writer.core.ingestion.repository import DocumentRepository
from smart_report_writer.core.generation.pipeline import generate_report_pipeline
from smart_report_writer.core.ingestion.storage import StorageClient
import boto3
from sqlalchemy.orm import sessionmaker
from common.db import get_engine

celery = Celery(__name__, broker=os.getenv("REDIS_URL"), backend=os.getenv("REDIS_URL"))
celery.conf.update(task_always_eager=False, task_track_started=True)

def enqueue_generate(req: GenerateRequest, settings: AppSettings) -> str:
    job_id = new_job_id()
    celery.send_task("worker.tasks.generate", args=[req.model_dump(), settings.model_dump(), job_id])
    set_status(job_id, "queued", message="Job enqueued")
    return job_id

@celery.task(name="worker.tasks.generate")
def generate(req: Dict[str, Any], settings_dict: Dict[str, Any], job_id: str):
    settings = AppSettings(**settings_dict)
    set_status(job_id, "running", message="In progress")

    engine = get_engine(settings)
    Session = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
        use_ssl=settings.s3_secure,
    )
    storage = StorageClient(s3, bucket=settings.s3_bucket)
    repo = DocumentRepository(Session())

    try:
        result = generate_report_pipeline(GenerateRequest(**req), repo=repo, storage=storage, settings=settings)
        set_status(job_id, "succeeded", message="Done", artifact_url=result.download_url)
    except Exception as e:
        set_status(job_id, "failed", message=str(e))
        raise
