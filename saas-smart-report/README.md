# Smart Report Writer — Production-Ready Monorepo

This repo packages **API (FastAPI)**, **Worker (Celery)**, **UI (Streamlit)**, with **Postgres**, **MinIO**, **Redis**, and **Ollama** (either host or internal). It reuses the core library under `smart_report_writer/` as a local dependency in dev, and installs it into the images for production builds.

## Quickstart (one command)

```bash
# Host Ollama on your machine at 11434:
#   1) Install Ollama: https://ollama.com/download
#   2) ollama pull llama3.2:latest
#   3) ollama serve  (default :11434)

cp .env.example .env
docker compose   -f docker-compose.yaml   -f docker-compose.override.dev.yml   -f docker-compose.override.env.yml   -f docker-compose.override.db.yml   -f docker-compose.override.minio.yml   -f docker-compose.override.redis.yml   -f docker-compose.override.ports.yml   up -d --build
```

Then:
- API: <http://localhost:8000/docs>
- UI: <http://localhost:8501>

## Dev Modes

### 1) Use Host Ollama
Set in `.env`:
```
OLLAMA_BASE_URL=http://host.docker.internal:11434
```
Compose: (same stack as quickstart)

### 2) Use Internal Ollama (no host ports)
Set in `.env`:
```
OLLAMA_BASE_URL=http://ollama:11434
```
Add the override:
```bash
docker compose   -f docker-compose.yaml   -f docker-compose.override.dev.yml   -f docker-compose.override.env.yml   -f docker-compose.override.db.yml   -f docker-compose.override.minio.yml   -f docker-compose.override.redis.yml   -f docker-compose.override.ports.yml   -f docker-compose.override.ollama.yml   up -d --build
```
Then inside `ollama` container:
```bash
docker compose exec ollama ollama pull llama3.2:latest
```

## One-liner up (deterministic order)
Recommended ordered sequence for clarity:
```bash
docker compose   -f docker-compose.yaml   -f docker-compose.override.dev.yml   -f docker-compose.override.env.yml   -f docker-compose.override.db.yml   -f docker-compose.override.redis.yml   -f docker-compose.override.minio.yml   -f docker-compose.override.ports.yml   up -d --build
```
Optionally append `-f docker-compose.override.ollama.yml`.

## Verify API ↔ Ollama connectivity (from API container)

```bash
docker compose exec api python - <<'PY'
import os, urllib.request, json
base = os.environ.get("OLLAMA_BASE_URL","http://ollama:11434")
print("Testing:", base)
req=urllib.request.Request(base+"/api/tags")
with urllib.request.urlopen(req, timeout=5) as r:
    print("OK status:", r.status)
    data=json.loads(r.read().decode())
    print("Models:", [m["name"] for m in data.get("models",[])])
PY
```

## Seed benchmark files (optional)
```bash
mkdir -p bench/docs
cp smart_report_writer/smart_report_writer/bench/docs/* bench/docs/ 2>/dev/null || true
```

## Submit a test job & poll
```bash
# Create job
JOB_ID=$(curl -s -X POST "http://localhost:8000/jobs"   -H "Authorization: Bearer devtoken-please-dont-use-in-prod"   -H "Content-Type: application/json"   -d '{"sources":["s3://srw-artifacts/demo/sample1.pdf"],"template":null}' | jq -r .job_id)

# Poll
watch -n 2 "curl -s -H 'Authorization: Bearer devtoken-please-dont-use-in-prod' http://localhost:8000/jobs/$JOB_ID | jq"
```

## Notes & Assumptions
- `smart_report_writer/` is treated as **local editable** in dev via `PYTHONPATH=/app:/opt/srw` and mounted at `/opt/srw`.
- In prod builds, the Dockerfiles **copy** `smart_report_writer/` into the image and `pip install` it.
- Dev auth uses a static bearer token (`JWT_DEV_BEARER`).
- Minimal row scoping included; for dev we use a single org/user.

See: `TUTORIALS/` and `DEBUGGING.md` for detailed flows.
