from datetime import timedelta
import os
from urllib.parse import urlparse, urlunparse

def _rewrite_public_base(url: str) -> str:
    base = os.getenv("MINIO_PUBLIC_BASE")
    if not base:
        return url
    u = urlparse(url)
    b = urlparse(base)
    return urlunparse((b.scheme, b.netloc, u.path, u.params, u.query, u.fragment))

import io
from minio import Minio
from common.config import settings

def get_s3():
    return Minio(
        endpoint=settings.s3_endpoint.replace("http://","").replace("https://",""),
        access_key=settings.s3_access_key,
        secret_key=settings.s3_secret_key,
        secure=settings.s3_endpoint.startswith("https://"),
    )

def bucket(): return settings.s3_bucket

def presign_put(key: str, mime: str, expires=3600):
    s3 = get_s3()
    return s3.presigned_put_object(bucket(), key, expires=timedelta(seconds=expires))

def presign_get(key: str, expires=3600):
    s3 = get_s3()
    return s3.presigned_get_object(bucket(), key, expires=timedelta(seconds=expires))

def put_object(key: str, data: bytes, mime_type="application/octet-stream"):
    s3 = get_s3()
    s3.put_object(bucket(), key, io.BytesIO(data), length=len(data), content_type=mime_type)

def s3_url_for(key: str):
    return f"s3://{bucket()}/{key}"
