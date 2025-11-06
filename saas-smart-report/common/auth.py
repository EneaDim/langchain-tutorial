from fastapi import Depends, HTTPException, Header
from pydantic import BaseModel
from common.config import settings

class DevUser(BaseModel):
    user_id: str = "dev"
    org_id: str = "devorg"
    allowed_mime: list[str] = [m.strip() for m in settings.allowed_mime_list.split(",") if m.strip()]

def require_auth(authorization: str = Header(None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = authorization.split(" ",1)[1].strip()
    if token != settings.jwt_dev_bearer:
        raise HTTPException(401, "Invalid token")
    return DevUser()
