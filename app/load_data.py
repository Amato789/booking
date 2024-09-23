import json
from datetime import datetime

from fastapi import APIRouter
from sqlalchemy import insert, select

from app.bookings.models import Bookings
from app.database import async_session_maker
from app.hotels.models import Hotels, Rooms
from app.images.models import HotelImages
from app.users.models import Users

router = APIRouter(
    prefix="/loaddata",
    tags=["Load Data to DB"],
)


@router.get("")
async def load_default_data_to_db():
    def open_json(model: str):
        with open(f"app/tests/mock_{model}.json", "r") as file:
            return json.load(file)

    hotels = open_json("hotels")
    rooms = open_json("rooms")
    users = open_json("users")
    bookings = open_json("bookings")
    hotel_images = open_json("hotelimages")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        for Model, values in [
            (Hotels, hotels),
            (Users, users),
        ]:
            query = select(Model).filter_by(id=1)
            result = await session.execute(query)
            existing_entry = result.scalar_one_or_none()
            if not existing_entry:
                query = insert(Model).values(values)
                await session.execute(query)

        await session.commit()

        for Model, values in [
            (Rooms, rooms),
            (Bookings, bookings),
            (HotelImages, hotel_images),
        ]:
            query = select(Model).filter_by(id=1)
            result = await session.execute(query)
            existing_entry = result.scalar_one_or_none()
            if not existing_entry:
                query = insert(Model).values(values)
                await session.execute(query)

        await session.commit()
