# Simple no-op placeholder; replace with Redis-based limiter in production
from fastapi import HTTPException

def check_rate_limit(user_id: str):
    # Implement token bucket using Redis for real use.
    return
