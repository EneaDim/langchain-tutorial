import redis
from app.core.config import settings

r = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

def get_cached(key: str):
    try:
        return r.get(key)
    except Exception:
        return None

def set_cached(key: str, value: str, ttl: int = 600):
    try:
        r.setex(key, ttl, value)
    except Exception:
        pass
