FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY api/workers/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY api/workers /app/api/workers
COPY common /app/common

COPY smart_report_writer /opt/srw
RUN pip install --no-cache-dir /opt/srw || true

ENV PYTHONUNBUFFERED=1

CMD ["celery","-A","api.workers.celery_app:celery_app","worker","--loglevel=INFO","-Q","default"]
