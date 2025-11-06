# Smart Report Writer SaaS — Rebuilt

This repository contains FastAPI (API), Celery (Worker), Streamlit (UI) around your `smart_report_writer` library.

## Quick Start (Host Ollama)

```bash
# Start stack with host Ollama
docker compose   -f docker-compose.yaml   -f docker-compose.override.fix-build.yml   -f docker-compose.override.dev.yml   -f docker-compose.override.redis.yml   -f docker-compose.override.minio.yml   -f docker-compose.override.db.yml   -f docker-compose.override.env.yml   -f docker-compose.override.ports.yml   up -d --build db redis minio createbucket api worker ui

curl -s http://localhost:8000/health/liveness
```

## Quick Start (Internal Ollama)

```bash
docker compose   -f docker-compose.yaml   -f docker-compose.override.fix-build.yml   -f docker-compose.override.dev.yml   -f docker-compose.override.redis.yml   -f docker-compose.override.minio.yml   -f docker-compose.override.db.yml   -f docker-compose.override.ollama.yml   -f docker-compose.override.env.yml   -f docker-compose.override.ports.yml   up -d --build ollama db redis minio createbucket api worker ui

docker exec -it saas-smart-report-writer-ollama-1 ollama pull llama3.2:latest
```

## Verify API → Ollama

```bash
docker exec -i saas-smart-report-writer-api-1 python - <<'PY'
import urllib.request, json
print(json.loads(urllib.request.urlopen("http://host.docker.internal:11434/api/version", timeout=5).read()))
PY
```

See `DEBUGGING.md` and `TUTORIALS/` for more.
