from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Reservation, Visitor, User
from .schemas import ReservationCreate


class ReservationRepository:
    @classmethod
    async def add_one_reservation(cls, session: AsyncSession, data: ReservationCreate) -> Reservation:
        reservation = Reservation(**data.model_dump())
        session.add(reservation)
        await session.commit()
        # await session.refresh(reservation)
        return reservation

    @classmethod
    async def find_all_reservation(cls, session: AsyncSession) -> list[Reservation]:
        stmt = select(Reservation).order_by(Reservation.id)
        result: Result = await session.execute(stmt)
        reservations = result.scalars().all()
        return list(reservations)

    @classmethod
    async def find_reservation(cls, session: AsyncSession, reservation_id: int) -> Reservation | None:
        return await session.get(Reservation, reservation_id)

    @classmethod
    async def find_reservation_user(cls, session: AsyncSession, user_id: int) -> list[Reservation]:
        stmt = (
            select(Reservation)
            .join(Visitor, Reservation.visitor_id == Visitor.id)
            .join(User, Visitor.user_id == User.id)
            .where(User.id == user_id)
        )
        result: Result = await session.execute(stmt)
        reservations = result.scalars().all()
        return list(reservations)
