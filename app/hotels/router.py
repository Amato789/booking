from datetime import date, datetime

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO, RoomDAO
from app.hotels.schemas import HotelInfoSchemas, HotelSchemas, RoomSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels&Rooms"],
)


@router.get("")
@cache(expire=10)
async def get_hotels_by_location_and_date(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(
            ...,
            description=f"Например, {datetime.now().date()}"
        )
) -> list[HotelInfoSchemas]:
    return await HotelDAO.find_all(
        location=location,
        date_from=date_from,
        date_to=date_to
    )


@router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int) -> list[HotelSchemas]:
    hotel = await HotelDAO.find_by_id(hotel_id)
    return hotel


@router.get("/{hotel_id}/rooms")
@cache(expire=20)
async def get_rooms(hotel_id: int) -> list[RoomSchema]:
    return await RoomDAO.find_all(hotel_id=hotel_id)
