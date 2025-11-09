from fastapi import APIRouter, Query
from sqlalchemy import text
from app.models.db import SessionLocal
from app.schemas import JobOut

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("", response_model=list[JobOut])
def list_jobs(limit: int = Query(10, ge=1, le=100)):
    with SessionLocal() as db:
        rows = db.execute(
            text("SELECT id, filename, summary FROM jobs ORDER BY id DESC LIMIT :l"),
            {"l": limit}
        ).fetchall()
    return [
        JobOut(id=r.id, filename=r.filename, summary=r.summary[:200])
        for r in rows
    ]
