from celery import Celery
from celery.schedules import crontab

from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.tasks.scheduled",
    ]
)

celery.conf.broker_connection_retry_on_startup = True

celery.conf.beat_schedule = {
    "check_in_remainder_1": {
        "task": "check_in_remainder_tomorrow",
        "schedule": 30,
        # "schedule": crontab(minute="0", hour="9"),
    },
    "check_in_remainder_2": {
        "task": "check_in_remainder_in_three_days",
        "schedule": crontab(minute='30', hour='15'),
    }
}
