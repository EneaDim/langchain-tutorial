from functools import lru_cache
from smart_report_writer.core.models.settings import AppSettings
from common.db import get_engine, get_sessionmaker
from smart_report_writer.core.ingestion.storage import StorageClient
import boto3
import os

@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()

def get_db_session():
    settings = get_settings()
    Session = get_sessionmaker(get_engine(settings))
    with Session() as s:
        yield s

def get_storage():
    settings = get_settings()
    s3 = boto3.client(
        "s3",
        endpoint_url=settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key,
        aws_secret_access_key=settings.s3_secret_key,
        region_name=settings.s3_region,
        use_ssl=settings.s3_secure,
    )
    return StorageClient(s3, bucket=settings.s3_bucket)
