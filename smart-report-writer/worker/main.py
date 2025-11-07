from multiprocessing import Process
from worker.heartbeat import run_heartbeat
from worker.tasks import celery

if __name__ == "__main__":
    hb = Process(target=run_heartbeat, args=(5556,))
    hb.daemon = True
    hb.start()
    celery.worker_main(argv=["worker", "--loglevel=INFO", "--concurrency=2"])
