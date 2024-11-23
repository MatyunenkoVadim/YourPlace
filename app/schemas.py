from email.policy import strict

from dulwich.config import ConfigDict
from pydantic import BaseModel


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
