from datetime import datetime

import pytest

from app.bookings.dao import BookingDAO


@pytest.mark.parametrize("user_id, room_id", [
    (2, 2),
    (2, 3),
    (1, 4),
    (1, 4),
])
async def test_booking_crud(user_id, room_id):
    # check add booking
    new_booking = await BookingDAO.add(
        user_id=user_id,
        room_id=room_id,
        date_from=datetime.strptime("2024-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-07-24", "%Y-%m-%d"),
    )
    assert new_booking.user_id == user_id
    assert new_booking.room_id == room_id

    # check find booking
    new_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert new_booking is not None

    # check delete booking
    await BookingDAO.remove(booking_id=new_booking.id, user_id=user_id)
    deleted_booking = await BookingDAO.find_one_or_none(id=new_booking.id)
    assert deleted_booking is None
