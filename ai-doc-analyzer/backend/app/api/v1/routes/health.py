from fastapi import APIRouter
from sqlalchemy import text
from app.models.db import SessionLocal
from app.services.cache import get_cached

router = APIRouter(tags=["health"])

@router.get("/healthz")
def healthz():
    return {"status": "ok"}

@router.get("/ready")
def ready():
    # DB check
    try:
        with SessionLocal() as db:
            db.execute(text("SELECT 1"))
    except Exception as e:
        return {"status": "error", "component": "db", "detail": str(e)}
    # Redis check (access path)
    try:
        _ = get_cached("__ping__")
    except Exception as e:
        return {"status": "error", "component": "redis", "detail": str(e)}
    return {"status": "ready"}
