from celery import Celery

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "aurora_core",
    broker=settings.broker_url,
    backend=settings.result_backend,
    include=["app.workers.tasks"],
)
celery_app.conf.task_default_queue = "aurora"
celery_app.conf.task_track_started = True
celery_app.conf.broker_connection_retry_on_startup = True
