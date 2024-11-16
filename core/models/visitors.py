from sqlalchemy.orm import Mapped

from core.models.model import Model


class VisitorsTable(Model):
    __tablename__ = "visitors"

    name: Mapped[str]
    phone: Mapped[str]