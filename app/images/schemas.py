from pydantic import BaseModel


class HotelImagesSchemas(BaseModel):
    id: int
    hotel_id: int
    name: str
