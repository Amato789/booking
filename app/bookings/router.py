from fastapi import APIRouter, Depends
from app.bookings.service import BookingService
from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema, NewBookingSchema
from app.exceptions import RoomCannotBeBooked
from app.users.models import Users
from app.users.dependencies import get_current_user
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
    new_booking = await BookingService.add_booking(booking=booking, user=user)
    return new_booking


@router.delete("/{booking_id}")
@version(2)
async def remove_booking(booking_id: int, user: Users = Depends(get_current_user)) -> None:
    await BookingDAO.remove(user_id=user.id, booking_id=booking_id)
