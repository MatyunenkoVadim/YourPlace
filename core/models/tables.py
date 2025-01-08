"""
Этот модуль определяет модель Table, которая представляет стол в системе.

Классы:
- Table: Модель, представляющая стол, включая количество мест.

Зависимости:
- Использует SQLAlchemy для определения моделей и отношений.
- Использует типы из typing для проверки типов во время разработки.

Контекст:
Этот файл является частью системы управления столами и используется для
хранения и управления данными о столах в базе данных.
"""

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship
from .model import Model
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .reservations import Reservation


class Table(Model, IdIntPkMixin):
    """
    Модель, представляющая стол в системе.

    Атрибуты:
    - number_seats: Количество мест за столом.
    - reservation: Бронирование, связанное со столом.
    """

    __tablename__ = "tables"

    number_seats: Mapped[int]

    reservation: Mapped["Reservation"] = relationship(back_populates="table")
