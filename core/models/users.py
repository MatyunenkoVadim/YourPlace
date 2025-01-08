"""
Этот модуль определяет модель User, которая представляет пользователя в системе.

Классы:
- User: Модель, представляющая пользователя, включая телефон и полное имя.

Зависимости:
- Использует SQLAlchemy для определения моделей и отношений.
- Использует FastAPI Users для интеграции с базой данных пользователей.
- Использует типы из typing для проверки типов во время разработки.

Контекст:
Этот файл является частью системы управления пользователями и используется для
хранения и управления данными о пользователях в базе данных.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model import Model
from typing import TYPE_CHECKING
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .visitors import Visitor


class User(Model, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    """
    Модель, представляющая пользователя в системе.

    Атрибуты:
    - phone: Номер телефона пользователя, уникальный для каждого пользователя.
    - fullname: Полное имя пользователя.
    - is_admin: Наличие прав администратора
    - visitor:
    """

    __tablename__ = "users"

    phone: Mapped[str | None] = mapped_column(unique=True)
    fullname: Mapped[str | None]
    is_admin: Mapped[bool] = mapped_column(default=False)
    visitor: Mapped[list["Visitor"]] = relationship(back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        """
        Возвращает объект SQLAlchemyUserDatabase для взаимодействия с базой данных пользователей.

        Параметры:
        - session: Асинхронная сессия SQLAlchemy.

        Возвращает:
        - Объект SQLAlchemyUserDatabase, связанный с моделью пользователя.
        """
        return SQLAlchemyUserDatabase(session, cls)
