from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    phone: str | None = None
    full_name: str | None = None


class UserInDB(User):
    id: int
    hashed_password: str
    active: bool = True


class UserAuth(User):
    hashed_password: bytes
    active: bool = True
