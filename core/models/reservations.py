from datetime import datetime

from sqlalchemy.orm import Mapped

from core.models import Model


class ReservationsTable(Model):
    __tablename__ = "reservation"

    guest_count: Mapped[int]
    reservation_date: Mapped[datetime]
    table_number: Mapped[str]