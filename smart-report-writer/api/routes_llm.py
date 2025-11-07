from fastapi import APIRouter
from smart_report_writer.core.models.llm import Provider, LLMConfig

router = APIRouter(prefix="/v1/llm", tags=["llm"])

@router.get("/providers")
def providers():
    return {"data": [p.value for p in Provider], "error": None, "meta": {}}

@router.get("/defaults")
def defaults():
    cfg = LLMConfig()
    return {"data": cfg.model_dump(), "error": None, "meta": {}}
