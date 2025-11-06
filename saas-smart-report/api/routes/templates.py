from fastapi import APIRouter, Depends
from common.auth import require_auth

router = APIRouter()

@router.get("")
def list_templates(user=Depends(require_auth)):
    return [
        {"id":"none","name":"No Template (.md output only)"},
        {"id":"template_a","name":"Template A (.docx enabled)"},
        {"id":"template_b","name":"Template B (.docx enabled)"},
    ]
