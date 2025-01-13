from celery import Celery


celery_worker = Celery(
    "celery",
    broker="redis://lowry-redis:6379/0",
    backend="redis://lowry-redis:6379/0",
)

celery_worker.conf.broker_connection_retry_on_startup = True

celery_worker.autodiscover_tasks(["src.tasks.standard_tasks"])