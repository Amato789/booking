from app.tasks.celery_setup import celery
from datetime import datetime


# @celery.task(name="periodic_task")
# def periodic_task():
#     print(12345)


@celery.task(name="check_in_remainder_tomorrow")
def check_in_remainder_tomorrow():
    print("Сейчас хззз")


@celery.task(name="check_in_remainder_in_three_days")
def check_in_remainder_in_three_days():
    print(f"Сейчас {datetime.now()}")
