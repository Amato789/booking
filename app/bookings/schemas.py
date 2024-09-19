from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo
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

    @field_validator("date_to")
    def check_dates(cls, date_to: date, info: ValidationInfo):
        date_from = info.data.get("date_from")
        if date_from and date_to <= date_from:
            raise ValueError("`date_to` must be greater than `date_from`")
        return date_to
