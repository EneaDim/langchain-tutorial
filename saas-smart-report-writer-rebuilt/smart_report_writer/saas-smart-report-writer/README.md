# SaaS Smart Report Writer (Streamlit + FastAPI + Celery)

**Production-ready skeleton** to serve the modular `smart_report_writer` library as a SaaS:

- Streamlit UI (`/ui`)
- FastAPI API (`/api`)
- Celery Worker (`/api/workers`)
- Multi-tenant metadata (Postgres) + S3/MinIO storage + Redis
- Docker Compose for local, Helm chart for k8s

> This is a working baseline you can extend. It *reuses* the Smart Report Writer you already built:
> install it in the worker/API environment (e.g., `pip install -e ../smart_report_writer`).

## Quickstart (Local)

```bash
cp .env.example .env
docker compose up --build
```

Open:
- UI: http://localhost:8501
- API docs: http://localhost:8000/docs
- MinIO console: http://localhost:9001  (minio / minio123)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / admin)
```

### Minimal Workflow

1) In UI, upload files, pick topic/model/template.
2) Click **Run** to create a job; worker builds summaries (calls your library).
3) Download `summary.md`, `report.md`, and optional `.docx`.

## Reuse your existing library

By default, the worker tries to import `smart_report_writer` and call its CLI via subprocess for maximum compatibility.
If not present, the task will fail with a clear message.

Install the library in the worker container by adding to `api/workers/Dockerfile`:
```
# inside the worker Dockerfile build stage
# COPY ../smart_report_writer /opt/smart_report_writer
# RUN pip install -e /opt/smart_report_writer
```

## Structure
See repo tree and inline docstrings for more details.
