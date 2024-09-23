from pydantic import TypeAdapter

from app.bookings.dao import BookingDAO
from app.bookings.schemas import NewBookingSchema
from app.exceptions import RoomCannotBeBooked
from app.tasks.tasks import send_booking_confirmation_email
from app.users.models import Users


class BookingService:
    @classmethod
    async def add_booking(
            cls,
            booking: NewBookingSchema,
            user: Users,
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
        send_booking_confirmation_email.delay(booking, user.email)
        return booking
