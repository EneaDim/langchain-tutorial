from celery import Celery
import os

broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
backend_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery = Celery("srw", broker=broker_url, backend=backend_url)
celery.conf.task_routes = {"api.workers.tasks.*": {"queue": "summarize"}}
