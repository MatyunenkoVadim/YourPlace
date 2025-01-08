"""
Этот модуль определяет репозиторий для работы с бронированиями в базе данных.

Классы:
- ReservationRepository: Класс, предоставляющий методы для добавления и поиска бронирований.

Зависимости:
- Использует SQLAlchemy для работы с базой данных.
- Использует модели Reservation, Visitor и User для представления данных.

Контекст:
Этот файл является частью системы управления бронированиями и используется для
выполнения операций с бронированиями в базе данных.
"""

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Reservation, Visitor, User
from .schemas import ReservationCreate


class ReservationRepository:
    """
    Класс, предоставляющий методы для добавления и поиска бронирований.
    """

    @classmethod
    async def add_one_reservation(cls, session: AsyncSession, data: ReservationCreate) -> Reservation:
        """
        Добавляет новое бронирование в базу данных.

        Параметры:
        - session: Асинхронная сессия SQLAlchemy.
        - data: Данные для создания нового бронирования.

        Возвращает:
        - Объект Reservation, представляющий добавленное бронирование.
        """
        reservation = Reservation(**data.model_dump())
        session.add(reservation)
        await session.commit()
        # await session.refresh(reservation)
        return reservation

    @classmethod
    async def find_all_reservation(cls, session: AsyncSession) -> list[Reservation]:
        """
        Находит все бронирования в базе данных.

        Параметры:
        - session: Асинхронная сессия SQLAlchemy.

        Возвращает:
        - Список объектов Reservation, представляющих все бронирования.
        """
        stmt = select(Reservation).order_by(Reservation.id)
        result: Result = await session.execute(stmt)
        reservations = result.scalars().all()
        return list(reservations)

    @classmethod
    async def find_reservation(cls, session: AsyncSession, reservation_id: int) -> Reservation | None:
        """
        Находит бронирование по его идентификатору.

        Параметры:
        - session: Асинхронная сессия SQLAlchemy.
        - reservation_id: Идентификатор бронирования.

        Возвращает:
        - Объект Reservation, если бронирование найдено, иначе None.
        """
        return await session.get(Reservation, reservation_id)

    @classmethod
    async def find_reservation_user(cls, session: AsyncSession, user_id: int) -> list[Reservation]:
        """
        Находит все бронирования, связанные с определенным пользователем.

        Параметры:
        - session: Асинхронная сессия SQLAlchemy.
        - user_id: Идентификатор пользователя.

        Возвращает:
        - Список объектов Reservation, связанных с пользователем.
        """
        stmt = (
            select(Reservation)
            .join(Visitor, Reservation.visitor_id == Visitor.id)
            .join(User, Visitor.user_id == User.id)
            .where(User.id == user_id)
        )
        result: Result = await session.execute(stmt)
        reservations = result.scalars().all()
        return list(reservations)
