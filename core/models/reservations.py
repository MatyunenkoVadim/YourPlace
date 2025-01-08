"""
Этот модуль определяет модель Reservation, которая представляет бронирование в системе.

Классы:
- Reservation: Модель, представляющая бронирование, включая количество гостей, дату бронирования,
  номер стола и идентификатор посетителя.

Зависимости:
- Использует SQLAlchemy для определения моделей и отношений.
- Использует типы из typing для проверки типов во время разработки.

Контекст:
Этот файл является частью системы управления бронированиями и используется для
хранения и управления данными о бронированиях в базе данных.
"""

from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model import Model
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .visitors import Visitor
    from .tables import Table


class Reservation(Model, IdIntPkMixin):
    """
    Модель, представляющая бронирование в системе.

    Атрибуты:
    - guest_count: Количество гостей для бронирования.
    - reservation_date: Дата и время бронирования.
    - table_number: Номер стола, связанный с бронированием.
    - visitor_id: Идентификатор посетителя, связанного с бронированием.
    - visitor: Объект Visitor, связанный с бронированием.
    - table: Объект Table, связанный с бронированием.
    """

    __tablename__ = "reservations"

    guest_count: Mapped[int]
    reservation_date: Mapped[str]

    table_number: Mapped[int] = mapped_column(
        ForeignKey("tables.id"),
        unique=True,
    )
    visitor_id: Mapped[int] = mapped_column(
        ForeignKey("visitors.id"),
    )
    visitor: Mapped["Visitor"] = relationship(back_populates="reservations")
    table: Mapped["Table"] = relationship(back_populates="reservation")
