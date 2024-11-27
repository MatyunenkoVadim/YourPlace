from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    phone: str | None = None
    fullname: str | None = None


class UserInDB(User):
    id: int
    hashed_password: str
    active: bool = True


class UserAuth(User):
    hashed_password: bytes = Field(..., alias="password")
    active: bool = True

class UserRegister(BaseModel):
    username: str
    password: str
