import asyncio

from fastapi import APIRouter, Query
from pydantic import parse_obj_as

from app.hotels.schemas import HotelSchemas, HotelInfoSchemas, RoomSchema
from app.hotels.dao import HotelDAO, RoomDAO
from datetime import date, datetime
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels&Rooms"],
)


@router.get("")
async def get_hotels_by_location_and_date(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}")) -> list[HotelInfoSchemas]:
    return await HotelDAO.find_all(location=location, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}")
# @cache(expire=60)
async def get_hotel(hotel_id: int) -> list[HotelSchemas]:
    # await asyncio.sleep(3)
    hotel = await HotelDAO.find_by_id(hotel_id)
    return hotel


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int) -> list[RoomSchema]:
    return await RoomDAO.find_all(hotel_id=hotel_id)
