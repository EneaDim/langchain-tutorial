FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libmagic1 tesseract-ocr ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY common ./common
COPY smart_report_writer ./smart_report_writer
COPY worker ./worker
COPY config ./config

EXPOSE 5556
USER 65532:65532
ENTRYPOINT ["python", "-m", "worker.main"]
