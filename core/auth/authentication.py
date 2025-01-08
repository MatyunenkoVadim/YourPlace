"""
Этот модуль отвечает за аутентификацию и регистрацию пользователей в системе.

Функции:
- authenticate_user: Аутентифицирует пользователя по имени пользователя и паролю.
- get_current_token_payload_user: Извлекает полезную нагрузку из JWT токена.
- get_current_auth_user: Получает текущего аутентифицированного пользователя.
- get_current_auth_active_user: Проверяет, активен ли текущий пользователь.
- register_user: Регистрирует нового пользователя с хешированием пароля.

Зависимости:
- Использует FastAPI для обработки HTTP запросов и зависимостей.
- Использует SQLAlchemy для асинхронного взаимодействия с базой данных.
- Использует bcrypt для хеширования паролей.

Контекст:
Этот файл является частью модуля аутентификации в проекте и взаимодействует с
репозиторием пользователей для выполнения операций с базой данных.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from fastapi import Form, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from api_v1.users.schemas import UserAuth, UserRegister, UserInDB
from core.secure import hashed as auth_password
from core.auth import utils as auth_utils
from core.models.db_helper import db_helper

from api_v1.users.db_controller import UsersRepository

import bcrypt

# HTTPBearer используется для аутентификации через заголовок Authorization
http_bearer = HTTPBearer()


async def authenticate_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    Аутентификация пользователя по имени пользователя и паролю.
    """
    # Исключение для неавторизованного доступа
    unauthed_exp = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    # Поиск пользователя в базе данных
    user = await UsersRepository.find_user(session=session, username=username)
    if not user:
        raise unauthed_exp

    # Проверка пароля
    if not auth_password.validate_password(
        password=password,
        hashed_password=user.password.encode(),
    ):
        raise unauthed_exp

    # Проверка, активен ли пользователь
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )
    return user


def get_current_token_payload_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    """
    Получение полезной нагрузки токена из заголовка Authorization.
    """
    token = credentials.credentials
    try:
        # Декодирование JWT токена
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
    """
    Получение текущего аутентифицированного пользователя на основе полезной нагрузки токена.
    """
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
    """
    Проверка, активен ли текущий аутентифицированный пользователь.
    """
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


async def register_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserRegister:
    """
    Регистрация нового пользователя с хешированием пароля.
    """
    # Хеширование пароля
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_auth = UserAuth(
        username=username,
        hashed_password=hashed_password,
    )

    try:
        # Создание нового пользователя в базе данных
        await UsersRepository.create_new_user(session=session, user_auth=user_auth)
        return UserRegister(
            username=user_auth.username,
            password=user_auth.hashed_password.decode(),
        )
    except IntegrityError as e:
        # Откат транзакции в случае ошибки
        await session.rollback()
        if "unique constraint" in str(e.orig).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username or phone already exists",
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
