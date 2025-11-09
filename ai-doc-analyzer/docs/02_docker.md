# 🐳 Docker Architecture

## 1. Services
| Service | Exposed | Internal | Description |
|----------|----------|-----------|--------------|
| UI | 8502 | 8501 | Streamlit frontend |
| Backend | 8000 | 8000 | FastAPI app |
| Postgres | — | 5432 | Database |
| Redis | — | 6379 | Cache |

## 2. Commands
```bash
docker compose build
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down -v
```

## 3. Volumes
Postgres uses the pgdata volume.
To reset:
```bash
docker compose down -v
```
