from sqlalchemy.orm import Mapped, mapped_column

from .model import Model

from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Model, IdIntPkMixin, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"

    phone: Mapped[str | None] = mapped_column(unique=True)
    fullname: Mapped[str | None]

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
