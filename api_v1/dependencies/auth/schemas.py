from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    phone: str | None
    fullname: str | None


class UserCreate(schemas.BaseUserCreate):
    phone: Optional[str] = None
    fullname: Optional[str] = None

class UserRegister(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    phone: Optional[str] = None
    fullname: Optional[str] = None
