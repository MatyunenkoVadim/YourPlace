from fastapi import Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from app.schemas import UserAuth
from secure import hashed as auth_password
from auth import utils as auth_utils

http_bearer = HTTPBearer()

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

def get_current_token_payload_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )
    return payload

def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload_user),
) -> UserAuth:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid",
    )

def get_current_auth_active_user(
    user: UserAuth = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )