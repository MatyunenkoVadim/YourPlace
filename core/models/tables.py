from sqlalchemy.orm import Mapped

from core.models.model import Model


class TablesTable(Model):
    __tablename__ = "tables"

    number_seats: Mapped[int]