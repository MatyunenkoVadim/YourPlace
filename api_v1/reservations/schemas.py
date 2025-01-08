from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservationCreate(BaseModel):
    guest_count: int
    reservation_date: str
    table_number: int


class ReservationResponse(ReservationCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int