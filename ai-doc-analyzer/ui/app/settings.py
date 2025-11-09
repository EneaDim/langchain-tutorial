import os
APP_MODE = os.getenv("APP_MODE", "docker")
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))
# Priorità: BACKEND_URL (compose/Dockerfile) → API_URL (legacy) → default 'backend' service
BACKEND_URL = os.getenv("BACKEND_URL") or os.getenv("API_URL") or "http://backend:8000"
