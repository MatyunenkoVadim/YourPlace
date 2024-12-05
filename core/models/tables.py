from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .model import Model
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .reservations import Reservation


class Table(Model, IdIntPkMixin):
    __tablename__ = "tables"

    number_seats: Mapped[int]

    reservation: Mapped["Reservation"] = relationship(back_populates="table")