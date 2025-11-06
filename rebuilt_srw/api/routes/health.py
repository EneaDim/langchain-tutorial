from fastapi import APIRouter

router = APIRouter()

@router.get("/liveness")
def liveness():
    return {"status": "ok"}

@router.get("/readiness")
def readiness():
    return {"status": "ok"}
