# Use Host Ollama

- In `.env`:
  ```
  OLLAMA_BASE_URL=http://host.docker.internal:11434
  ```
- Verify from API container:
  ```bash
  docker compose exec api python - <<'PY'
import os, urllib.request
u=os.environ["OLLAMA_BASE_URL"]+"/api/tags"
print("GET", u)
print(urllib.request.urlopen(u).read()[:200])
PY
  ```
