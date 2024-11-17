from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .model import Model

if TYPE_CHECKING:
    from .reservations import Reservation


class Table(Model):
    __tablename__ = "tables"

    number_seats: Mapped[int]

    reservation: Mapped["Reservation"] = relationship(back_populates="table")