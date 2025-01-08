"""
Этот модуль определяет модель Visitor, которая представляет посетителя в системе.

Классы:
- Visitor: Модель, представляющая посетителя, включая имя и номер телефона.

Зависимости:
- Использует SQLAlchemy для определения моделей и отношений.
- Использует типы из typing для проверки типов во время разработки.

Контекст:
Этот файл является частью системы управления посетителями и используется для
хранения и управления данными о посетителях в базе данных.
"""

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .model import Model
from .mixins.id_int_pk import IdIntPkMixin

if TYPE_CHECKING:
    from .reservations import Reservation


class Visitor(Model, IdIntPkMixin):
    """
    Модель, представляющая посетителя в системе.

    Атрибуты:
    - name: Имя посетителя.
    - phone: Номер телефона посетителя, уникальный для каждого посетителя.
    - reservations: Список бронирований, связанных с посетителем.
    """

    __tablename__ = "visitors"

    name: Mapped[str]
    phone: Mapped[str] = mapped_column(unique=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="visitor")
