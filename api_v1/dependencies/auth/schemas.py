from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    is_admin: Optional[bool] = False
    phone: str | None
    fullname: str | None


class UserCreate(schemas.BaseUserCreate):
    is_admin: Optional[bool] = False
    phone: Optional[str] = None
    fullname: Optional[str] = None

class UserRegister(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    is_admin: Optional[bool] = False
    phone: Optional[str] = None
    fullname: Optional[str] = None
