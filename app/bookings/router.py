from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import BookingSchema, NewBookingSchema
from app.bookings.service import BookingService
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Booking"],
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[BookingSchema]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("")
async def add_booking(
        booking: NewBookingSchema,
        user: Users = Depends(get_current_user),
):
    new_booking = await BookingService.add_booking(booking=booking, user=user)
    return new_booking


@router.delete("/{booking_id}")
async def remove_booking(
        booking_id: int,
        user: Users = Depends(get_current_user)
) -> None:
    await BookingDAO.remove(user_id=user.id, booking_id=booking_id)
