from fastapi import APIRouter
import yaml
from pathlib import Path

router = APIRouter(prefix="/v1/templates", tags=["templates"])

@router.get("")
def list_templates():
    cfg = yaml.safe_load((Path("config/templates.yml")).read_text())
    return {"data": cfg, "error": None, "meta": {}}
