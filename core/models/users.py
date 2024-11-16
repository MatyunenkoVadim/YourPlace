from sqlalchemy.orm import Mapped

from core.models import Model


class UsersTable(Model):
    __tablename__ = "users"

    username: Mapped[str]
    phone: Mapped[str]
    fullname: Mapped[str]
    password: Mapped[str]