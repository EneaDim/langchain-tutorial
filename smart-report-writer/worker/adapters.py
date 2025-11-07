import os
from redis import Redis
from typing import Dict, Any
from uuid import uuid4

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = Redis.from_url(redis_url, decode_responses=True)

job_store: Dict[str, Any] = {}

def new_job_id() -> str:
    return uuid4().hex

def set_status(job_id: str, status: str, **kw):
    payload = {"job_id": job_id, "status": status, **kw}
    job_store[job_id] = payload
    r.hset(f"job:{job_id}", mapping=payload)
