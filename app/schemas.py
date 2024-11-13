from email.policy import strict

from dulwich.config import ConfigDict
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
    phone: str | None = None
    full_name: str | None = None

class UserInDB(User):
    id: int
    hashed_password: str

class UserAuth(User):
    model_config = ConfigDict()

    hashed_password: bytes
    active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
