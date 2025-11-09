import os

# Modalità di esecuzione (solo informativa)
APP_MODE = os.getenv("APP_MODE", "docker")

# Limite upload (MB)
MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "25"))

# URL del backend: supporta sia API_URL sia BACKEND_URL
BACKEND_URL = os.getenv("API_URL") or os.getenv("BACKEND_URL") or "http://backend:8000"
