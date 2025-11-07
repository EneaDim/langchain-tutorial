FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Minimal tools + curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY api ./api
COPY smart_report_writer ./smart_report_writer
COPY common ./common
COPY config ./config

EXPOSE 8080

# Healthcheck matches compose health probe
HEALTHCHECK --interval=5s --timeout=3s --retries=20 CMD curl -sf http://localhost:8080/healthz || exit 1

# Default command (dev override can replace this)
CMD ["uvicorn","api.main:app","--host","0.0.0.0","--port","8080"]
