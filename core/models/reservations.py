from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .model import Model
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .visitors import Visitor
    from .tables import Table

class Reservation(Model, IdIntPkMixin):
    __tablename__ = "reservations"

    guest_count: Mapped[int]
    reservation_date: Mapped[datetime]

    table_number: Mapped[int] = mapped_column(
        ForeignKey("tables.id"),
        unique=True,
    )
    visitor_id: Mapped[int] = mapped_column(
        ForeignKey("visitors.id"),
    )
    visitor: Mapped["Visitor"] = relationship(back_populates="reservations")
    table: Mapped["Table"] = relationship(back_populates="reservation")
