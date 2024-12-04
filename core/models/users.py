from sqlalchemy.orm import Mapped, mapped_column

from .model import Model

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
# TODO: Решить вопрос с UserIdType
# from core.types.user_id import UserIdType
# from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

# TODO: Создать класс IdIntPkMixin
class UserDB(Model, SQLAlchemyBaseUserTable[int]):
# class UserDB(Model, SQLAlchemyBaseUserTable[UserIdType]):
    __tablename__ = "users"

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)


class User(Model):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str | None] = mapped_column(unique=True)
    fullname: Mapped[str | None]
    password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)