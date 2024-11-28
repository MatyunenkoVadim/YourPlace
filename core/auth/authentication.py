from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from api_v1.users.schemas import UserAuth
from core.secure import hashed as auth_password
from core.auth import utils as auth_utils
from core.models.db_helper import db_helper

from api_v1.users.db_controller import UsersRepository

http_bearer = HTTPBearer()

# mark = UserAuth(
#     username="mark",
#     hashed_password=auth_password.hash_password("secret"),
#     phone="",
# )
# admin = UserAuth(
#     username="admin",
#     hashed_password=auth_password.hash_password("admin"),
#     phone="",
# )
#
# users_db: dict[str, UserAuth] = {
#     mark.username: mark,
#     admin.username: admin,
# }


async def authenticate_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = await UsersRepository.find_user(session=session, username=username)
    if not user:
        raise unauthed_exp

    if not auth_password.validate_password(
        password=password,
        hashed_password=user.password.encode(),
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

async def get_current_auth_user(
        payload: dict = Depends(get_current_token_payload_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> UserAuth:
    username: str | None = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )
    user = await UsersRepository.find_user(session=session, username=username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token invalid",
        )
    return user

async def get_current_auth_active_user(
    user: UserAuth = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )