"""
Этот модуль определяет схемы данных для работы с бронированиями, включая создание
и ответ на запросы бронирования.

Классы:
- ReservationCreate: Схема для создания нового бронирования.
- ReservationResponse: Схема для ответа с данными о бронировании.

Зависимости:
- Использует Pydantic для валидации и управления данными.

Контекст:
Этот файл является частью системы управления бронированиями и используется для
определения схем данных, которые используются в API для работы с бронированиями.
"""

from pydantic import BaseModel, ConfigDict


class ReservationCreate(BaseModel):
    """
    Схема для создания нового бронирования.

    Атрибуты:
    - guest_count: Количество гостей для бронирования.
    - reservation_date: Дата бронирования в формате строки.
    - table_number: Номер стола для бронирования.
    """
    guest_count: int
    reservation_date: str
    table_number: int


class ReservationResponse(ReservationCreate):
    """
    Схема для ответа с данными о бронировании.

    Атрибуты:
    - id: Идентификатор бронирования.
    """
    model_config = ConfigDict(from_attributes=True)
    id: int
