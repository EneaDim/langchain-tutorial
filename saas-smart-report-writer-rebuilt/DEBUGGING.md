# DEBUGGING

Common issues and fixes.

## Containers don’t start
- Check env:
  - `.env` present?
  - `OLLAMA_BASE_URL` reachable?
- `docker compose ps` and `docker compose logs <svc>`.

## API 500 or 422
- Ensure DB is reachable:
  - `docker compose exec api python -c "import sqlalchemy; print('ok')"`
  - `docker compose exec api python - <<'PY'
from common.db import engine
with engine.connect() as c: print('db ok', c)
PY`

## Ollama Errors
- **ECONNREFUSED**: wrong base URL. Host vs internal mismatch.
- **No model found**: `docker compose exec ollama ollama pull llama3.2:latest`.
- **Timeouts**: increase `CELERY_TASK_TIME_LIMIT` or set `SRW_TOTAL_CAP` lower.

## MinIO / S3
- Check that bucket exists:
  - `docker compose logs createbucket`
- Re-create bucket if needed:
  - `mc config host add local http://localhost:9000 minio minio123`
  - `mc mb local/srw-artifacts || true`
- Credentials: `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_REGION`.

## Postgres
- Healthcheck stuck? Wait for init.
- Connect:
  ```bash
  docker compose exec db psql -U postgres -d srw -c '\dt'
  ```

## Redis / Celery
- Ping redis: `docker compose exec redis redis-cli PING`
- Inspect Celery:
  - Logs: `docker compose logs worker`
  - Task states: look at `/jobs/{id}` API

## Dependency pinning
- We pin:
  - `langchain-ollama==0.2.0`
  - `langchain-core>=0.3,<0.4`
  - `pydantic>=2.4`
  - SQLAlchemy 2.x
- If resolver issues appear, clear caches and rebuild:
  ```bash
  docker compose build --no-cache api worker ui
  ```

## Networking matrix
- Host Ollama: containers → `http://host.docker.internal:11434`
- Internal Ollama: containers → `http://ollama:11434` (no host port)
- UI → API: `STREAMLIT_API_BASE` defaults to `http://localhost:8000` for host.
