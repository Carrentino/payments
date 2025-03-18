from celery import Celery
from celery.schedules import crontab

from .settings import get_settings
from .tasks.sync_balances import sync_balances_task  # noqa

celery_app = Celery(
    "payments",
    broker=f'{get_settings().redis.url}/{get_settings().redis.celery_db}',
)

celery_app.conf.beat_schedule = {
    "sync-balances-every-day": {
        "task": "sync_balances_task",
        "schedule": crontab(minute="0", hour="0"),
    },
}
