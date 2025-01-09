from celery import Celery


celery_worker = Celery(
    "celery",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery_worker.conf.broker_connection_retry_on_startup = True

celery_worker.autodiscover_tasks(["src.tasks.standard_tasks"])