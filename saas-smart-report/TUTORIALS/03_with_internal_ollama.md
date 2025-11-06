# Internal Ollama (no host ports)

1. Add compose override:
   ```bash
   docker compose      -f docker-compose.yaml      -f docker-compose.override.dev.yml      -f docker-compose.override.env.yml      -f docker-compose.override.db.yml      -f docker-compose.override.redis.yml      -f docker-compose.override.minio.yml      -f docker-compose.override.ports.yml      -f docker-compose.override.ollama.yml      up -d --build
   ```
2. Pull model inside:
   ```bash
   docker compose exec ollama ollama pull llama3.2:latest
   ```
3. Ensure `.env` has `OLLAMA_BASE_URL=http://ollama:11434`.
