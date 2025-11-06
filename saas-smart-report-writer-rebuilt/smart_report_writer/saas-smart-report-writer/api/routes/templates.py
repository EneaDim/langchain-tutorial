import uuid
from fastapi import APIRouter, Depends
from common.auth import require_auth

router = APIRouter()

# Stubs for CRUD; implement with DB + storage in production
@router.get("")
def list_templates(user=Depends(require_auth)):
    return [{"id": "tpl-a", "name": "Template A"}, {"id": "tpl-b", "name": "Template B"}]
