import os, pytest
os.environ["TESTING"]="1"
os.environ["DATABASE_URL"]="sqlite:///./test.db"  # semplice per unit test
os.environ["REDIS_URL"]="redis://localhost:6379/0"  # verrà sostituito con fake

from fastapi.testclient import TestClient
from app.main import app
from app.services import cache as cache_mod

class DummyRedis:
    _store = {}
    def get(self, k): return self._store.get(k)
    def setex(self, k, ttl, v): self._store[k] = v

cache_mod.r = DummyRedis()

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
