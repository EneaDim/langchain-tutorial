# 🗄️ PostgreSQL & Redis

## PostgreSQL
- DB: `ai_doc`
- User: `ai`
- Table: `jobs`

Example:
```bash
docker compose exec -T postgres psql -U ai -d ai_doc -c "\dt"
```

## Redis
Used for caching analyzed PDFs.

Key format:
```bash
analyze:<filename>:<len(content)>
```
Check keys:
```bash
docker compose exec -T redis redis-cli --scan
```
Clear cache
```bash
docker compose exec -T redis redis-cli FLUSHALL
```

