from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Form, HTTPException, status

from app.schemas import UserAuth
from secure import hashed as auth_password

mark = UserAuth(
    username="mark",
    hashed_password=auth_password.hash_password("secret"),
    phone="",
)
admin = UserAuth(
    username="admin",
    hashed_password=auth_password.hash_password("admin"),
    phone="",
)

users_db: dict[str, UserAuth] = {
    mark.username: mark,
    admin.username: admin,
}


def authenticate_user(
        username: str = Form(),
        password: str = Form(),
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if not (user := users_db.get(username)):
        raise unauthed_exp

    if not auth_password.validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise unauthed_exp

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user