import os
from celery import Celery

broker = os.environ.get("REDIS_URL", "redis://redis:6379/0")
backend = broker

celery_app = Celery("srw", broker=broker, backend=backend)
celery_app.conf.update(
    task_queues={"default": {}},
    task_default_queue="default",
    task_time_limit=3600,
    worker_cancel_long_running_tasks_on_connection_loss=True,
)
