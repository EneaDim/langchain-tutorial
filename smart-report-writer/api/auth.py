from fastapi import Header, HTTPException, Depends
import base64
import json
from typing import Optional

async def optional_jwt(authorization: Optional[str] = Header(default=None)):
    # Placeholder for OIDC/JWT verification if configured via env
    # For now, accept anonymous unless JWT_PUBLIC_KEY_BASE64 is set
    return {"sub": "anonymous"}
