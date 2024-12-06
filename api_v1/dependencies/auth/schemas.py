from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel

# from core.types.user_id import UserIdType


class UserRead(schemas.BaseUser[int]):
    username: str
    phone: str | None
    fullname: str | None


class UserCreate(schemas.BaseUserCreate):
    username: str
    phone: Optional[str] = None
    fullname: Optional[str] = None


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str] = None
    phone: Optional[str] = None
    fullname: Optional[str] = None


class UserRegisteredNotification(BaseModel):
    user: UserRead
    ts: int