from app.tasks.celery_setup import celery
from datetime import datetime
from app.bookings.dao import BookingDAO
import asyncio


async def get_data():
    print(await BookingDAO.get_bookings_by_date_from(days=3))


@celery.task(name="check_in_remainder_tomorrow")
def check_in_remainder_tomorrow():
    asyncio.run(get_data())


@celery.task(name="check_in_remainder_in_three_days")
def check_in_remainder_in_three_days():
    print(f"Now {datetime.now()}")
