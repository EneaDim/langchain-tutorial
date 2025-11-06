# Debugging

- `httpx.ConnectError`: API/Worker cannot reach Ollama.
- Missing env → Pydantic ValidationError: include `docker-compose.override.env.yml` in your compose command.
- Check logs: `docker compose logs -f api worker`.
