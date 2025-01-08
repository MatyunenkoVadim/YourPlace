"""
Этот модуль определяет зависимость для получения базы данных пользователей.

Функции:
- get_users_db: Возвращает базу данных пользователей для использования в FastAPI.

Зависимости:
- Использует FastAPI для управления зависимостями.
- Использует SQLAlchemy для работы с базой данных.

Контекст:
Этот файл является частью системы управления пользователями и используется для
предоставления базы данных пользователей, которая используется для операций с пользователями.
"""

from typing import TYPE_CHECKING, Annotated
from fastapi import Depends
from core.models import User
from core.models.db_helper import db_helper

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_helper.get_scoped_session),
    ],
):
    """
    Возвращает базу данных пользователей для использования в FastAPI.

    Параметры:
    - session: Асинхронная сессия SQLAlchemy, полученная через зависимость.

    Возвращает:
    - Объект базы данных пользователей, связанный с сессией.
    """
    yield User.get_db(session=session)
