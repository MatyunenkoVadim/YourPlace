from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model import Model
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .reservations import Reservation
    from .users import User


class Visitor(Model, IdIntPkMixin):
    __tablename__ = "visitors"

    name: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="visitor")
    user: Mapped[list["User"]] = relationship(back_populates="visitor")