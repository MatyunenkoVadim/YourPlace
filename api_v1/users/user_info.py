"""
Этот модуль определяет маршруты для управления пользователями, включая получение
информации о текущем пользователе и обновление данных пользователя.

Маршруты:
- Пользователи: Включает маршруты для получения и обновления данных пользователей.

Зависимости:
- Использует FastAPI для создания маршрутов.
- Использует FastAPI Users для управления пользователями.
- Использует SQLAlchemy для работы с базой данных.

Контекст:
Этот файл является частью системы управления пользователями и используется для
настройки маршрутов, связанных с пользователями, включая получение и обновление данных.
"""

from fastapi import APIRouter
from api_v1.users.fastapi_users_routes import fastapi_users
from api_v1.dependencies.auth.schemas import UserRead, UserUpdate
from core.config import settings

router = APIRouter(
    prefix=settings.users,
    tags=["Users"],
)

# Включает маршруты для получения и обновления данных пользователей, такие как /me и /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
