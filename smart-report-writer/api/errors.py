from fastapi import Request
from fastapi.responses import JSONResponse

def error_envelope(message: str, code: str = "bad_request", status: int = 400):
    return JSONResponse({"data": None, "error": {"code": code, "message": message}, "meta": {}}, status_code=status)

async def http_error_handler(request: Request, exc: Exception):
    return error_envelope(str(exc), "internal_error", 500)
