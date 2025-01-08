"""
Этот модуль определяет маршруты аутентификации и регистрации пользователей с использованием FastAPI Users.

Маршруты:
- Аутентификация: Включает маршруты для входа и выхода пользователей.
- Регистрация: Включает маршруты для регистрации новых пользователей.

Зависимости:
- Использует FastAPI для создания маршрутов.
- Использует FastAPI Users для управления аутентификацией и регистрацией.

Контекст:
Этот файл является частью системы аутентификации и используется для настройки
маршрутов, связанных с аутентификацией и регистрацией пользователей.
"""

from fastapi import APIRouter
from core.config import settings
from api_v1.dependencies.auth.backend import authentication_backend
from .fastapi_users_routes import fastapi_users
from api_v1.dependencies.auth.schemas import UserRead, UserRegister

router = APIRouter(
    prefix=settings.auth,
    tags=["Auth"],
)

# Включает маршруты для аутентификации пользователей, такие как /login и /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        # requires_verification=True,
    ),
)

# Включает маршруты для регистрации новых пользователей, такие как /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserRegister,
    ),
)
