"""
Этот модуль определяет маршруты для управления аутентификацией пользователей, включая
вход, регистрацию и получение информации о текущем пользователе.

Маршруты:
- auth_user_issue_jwt: Аутентифицирует пользователя и выдает JWT токен.
- auth_user_check_self_info: Возвращает информацию о текущем аутентифицированном пользователе.
- auth_user_register: Регистрирует нового пользователя и выдает JWT токен.

Зависимости:
- Использует FastAPI для создания маршрутов и управления зависимостями.
- Использует JWT для аутентификации пользователей.

Контекст:
Этот файл является частью системы аутентификации и используется для обработки
запросов пользователей на вход, регистрацию и получение информации о себе.
"""

from fastapi import APIRouter, Depends
from core.auth.schemas import Token
from api_v1.users.schemas import UserAuth, UserRegister
from core.auth.authentication import (
    authenticate_user,
    get_current_auth_active_user,
    get_current_token_payload_user,
    register_user,
)
from core.auth import utils as auth_utils

router = APIRouter(prefix="/users", tags=["Authorization"])


@router.post("/login", response_model=Token)
async def auth_user_issue_jwt(user: UserAuth = Depends(authenticate_user)):
    """
    Аутентифицирует пользователя и выдает JWT токен.

    Параметры:
    - user: Аутентифицированный пользователь.

    Возвращает:
    - Объект Token с JWT токеном и типом токена.
    """
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )


@router.get("/me")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload_user),
    user: UserAuth = Depends(get_current_auth_active_user),
):
    """
    Возвращает информацию о текущем аутентифицированном пользователе.

    Параметры:
    - payload: Полезная нагрузка JWT токена.
    - user: Текущий аутентифицированный пользователь.

    Возвращает:
    - Словарь с информацией о пользователе.
    """
    iat = payload.get("iat")
    return {
        "username": user.username,
        "phone": user.phone,
        "logged_in_at": iat,
    }


@router.post("/register", response_model=Token)
async def auth_user_register(user: UserRegister = Depends(register_user)):
    """
    Регистрирует нового пользователя и выдает JWT токен.

    Параметры:
    - user: Зарегистрированный пользователь.

    Возвращает:
    - Объект Token с JWT токеном и типом токена.
    """
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )