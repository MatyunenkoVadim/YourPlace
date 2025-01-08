"""
Этот модуль определяет зависимость для получения менеджера пользователей.

Функции:
- get_user_manager: Возвращает менеджер пользователей для использования в FastAPI.

Зависимости:
- Использует FastAPI для управления зависимостями.
- Использует SQLAlchemy для работы с базой данных пользователей.

Контекст:
Этот файл является частью системы управления пользователями и используется для
предоставления менеджера пользователей, который управляет операциями с пользователями.
"""

from typing import Annotated, TYPE_CHECKING
from fastapi import Depends
from core.auth.user_manager import UserManager
from .users import get_users_db

if TYPE_CHECKING:
    from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase


async def get_user_manager(
    users_db: Annotated[
        "SQLAlchemyUserDatabase",
        Depends(get_users_db),
    ]
):
    """
    Возвращает менеджер пользователей для использования в FastAPI.

    Параметры:
    - users_db: База данных пользователей, полученная через зависимость.

    Возвращает:
    - Экземпляр UserManager, управляющий операциями с пользователями.
    """
    yield UserManager(users_db)
