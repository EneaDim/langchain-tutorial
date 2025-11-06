# Local Dev (zero → running)

1. Install Docker Desktop.
2. Install Ollama and pull model:
   ```bash
   ollama pull llama3.2:latest
   ```
3. Copy env and bring up:
   ```bash
   cp .env.example .env
   docker compose      -f docker-compose.yaml      -f docker-compose.override.dev.yml      -f docker-compose.override.env.yml      -f docker-compose.override.db.yml      -f docker-compose.override.redis.yml      -f docker-compose.override.minio.yml      -f docker-compose.override.ports.yml      up -d --build
   ```
4. UI at <http://localhost:8501>, API at <http://localhost:8000>.
5. Upload files in UI, create a job, watch results.
