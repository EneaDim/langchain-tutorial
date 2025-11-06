import os, io, uuid, mimetypes, json
from typing import Optional
import boto3
from botocore.client import Config as BotoConfig
from .config import settings

_session = boto3.session.Session(
    aws_access_key_id=settings.s3_access_key,
    aws_secret_access_key=settings.s3_secret_key,
    region_name=settings.s3_region,
)
_s3 = _session.client(
    "s3",
    endpoint_url=settings.s3_endpoint,
    config=BotoConfig(signature_version="s3v4"),
)

def presign_put(file_id: str, content_type: str) -> dict:
    key = f"uploads/{file_id}"
    url = _s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": settings.s3_bucket, "Key": key, "ContentType": content_type},
        ExpiresIn=3600,
    )
    return {"url": url, "key": key}

def presign_get(key: str, expires: int = 3600) -> str:
    return _s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.s3_bucket, "Key": key},
        ExpiresIn=expires,
    )

def put_bytes(key: str, data: bytes, content_type: str):
    _s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=data, ContentType=content_type)
