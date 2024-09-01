from fastapi import APIRouter, Depends
from app.database import async_session_maker
from sqlalchemy import select
from app.bookings.models import Bookings
from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema, NewBookingSchema
from app.users.models import Users
from app.users.dependencies import get_current_user
from datetime import date
from app.exceptions import RoomCannotBeBooked
from fastapi_versioning import version
from pydantic import TypeAdapter


router = APIRouter(
    prefix="/bookings",
    tags=["Booking"],
)


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
@version(1)
async def add_booking(
        booking: NewBookingSchema,
        user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=booking.room_id,
        date_from=booking.date_from,
        date_to=booking.date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    booking = TypeAdapter(NewBookingSchema).validate_python(booking).model_dump()
    # TODO
    # add background tasks (celery)
    return booking


@router.delete("/{booking_id}")
@version(2)
async def remove_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.remove(user_id=user.id, booking_id=booking_id)
