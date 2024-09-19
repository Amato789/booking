import pytest
from httpx import AsyncClient
from app.bookings.dao import BookingDAO


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", *[
    [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
])
async def test_add_and_get_booking(
        room_id,
        date_from,
        date_to,
        booked_rooms,
        status_code,
        authenticated_ac: AsyncClient
):
    response = await authenticated_ac.post("/bookings", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms


async def test_add_and_delete_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.post("/bookings", json={
        "room_id": 5,
        "date_from": "2024-05-01",
        "date_to": "2024-05-15",
    })
    assert response.status_code == 200

    added_booking = await BookingDAO.find_one_or_none(user_id=1, room_id=5)
    assert added_booking is not None
    assert added_booking.id == 12

    response = await authenticated_ac.delete(f"/bookings/{added_booking.id}")
    assert response.status_code == 200
    deleted_booking = await BookingDAO.find_one_or_none(id=added_booking.id)
    assert deleted_booking is None
