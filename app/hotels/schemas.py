from typing import Optional

from pydantic import BaseModel
from app.images.schemas import HotelImagesSchemas


class HotelSchemas(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    images: str | None


class HotelInfoSchemas(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    rooms_available: int
    images: str | None


class RoomSchema(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list[str]
    quantity: int
    image_id: int
