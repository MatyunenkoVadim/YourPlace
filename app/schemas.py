from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    guest_count: int
    reservation_date: datetime
    table_number: str


class ReservationResponse(BaseModel):
    id: int
    guest_count: int
    reservation_date: datetime
    table_number: str

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
