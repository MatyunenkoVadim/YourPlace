from sqlalchemy.orm import Mapped, mapped_column

from .model import Model


class User(Model):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    fullname: Mapped[str | None]
    password: Mapped[str]