# ⚙️ Backend Core (FastAPI)

## 1. Endpoints
| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/analyze` | POST | Analyze PDF |
| `/jobs` | GET | List jobs |
| `/ready` | GET | Healthcheck with DB+Redis |
| `/healthz` | GET | Lightweight liveness |

## 2. Flow
1. Receive file
2. Check Redis for cache
3. If hit → return
4. Else → analyze text, save to DB, store cache

## 3. Example
```bash
curl -F "file=@sample.pdf" http://localhost:8000/analyze | python3 -m json.tool
```
