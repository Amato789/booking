import pytest
from httpx import AsyncClient


async def test_get_hotels_by_location_and_date(ac: AsyncClient):
    response = await ac.get("/hotels", params={
        "location": "Алтай",
        "date_from": "2024-09-10",
        "date_to": "2024-09-20",
    })
    assert response.status_code == 200
    if response.json():
        assert "Алтай" in response.json()[0]["location"]


@pytest.mark.parametrize("hotel_id, status_code", [
    (1, 200),
    (2, 200),
    (3, 200),
    (20, 200),
])
async def test_get_hotel(hotel_id, status_code, ac: AsyncClient):
    response = await ac.get(f"/hotels/{hotel_id}")
    assert response.status_code == status_code
    if response.json():
        assert response.json()[0]["id"] == hotel_id
