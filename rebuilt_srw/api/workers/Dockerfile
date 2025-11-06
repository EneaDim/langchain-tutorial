FROM python:3.11-slim
WORKDIR /app

COPY api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Add a non-root user
RUN useradd -ms /bin/bash appuser
USER appuser

COPY common /app/common
COPY api/workers /app/api/workers
# allow imports like api.workers...
COPY api /app/api

ENV PYTHONPATH=/app
CMD ["celery", "-A", "api.workers.celery_app.celery", "worker", "-Q", "summarize", "--loglevel=INFO"]
