from fastapi import APIRouter
from common.storage import get_s3
from common.db import engine
from sqlalchemy import text

router = APIRouter()

@router.get("/liveness")
def liveness():
    return {"status":"ok"}

@router.get("/readiness")
def readiness():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    s3 = get_s3()
    s3.list_buckets()
    return {"status":"ready"}
