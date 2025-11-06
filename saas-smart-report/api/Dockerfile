FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends     build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY api /app/api
COPY common /app/common

COPY smart_report_writer /opt/srw
RUN pip install --no-cache-dir /opt/srw || true

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

CMD ["python","-m","uvicorn","api.main:app","--host","0.0.0.0","--port","8000"]
