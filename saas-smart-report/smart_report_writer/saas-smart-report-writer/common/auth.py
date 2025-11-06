# Minimal stub for OIDC/JWT verification (replace with real verification)
from fastapi import Header, HTTPException

def require_auth(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    # In production: verify JWT against issuer JWKs, check audience, expiry, etc.
    # Here we accept any non-empty token and simulate a user/org.
    return {"user_id": "user-demo", "org_id": "org-demo", "email": "user@example.com", "is_admin": True}
