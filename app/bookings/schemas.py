from pydantic import BaseModel, ConfigDict
from datetime import date


class BookingSchema(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

    model_config = ConfigDict(from_attributes=True)


class NewBookingSchema(BaseModel):
    room_id: int
    date_from: date
    date_to: date
