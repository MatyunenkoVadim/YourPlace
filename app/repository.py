from sqlalchemy import select

from app.schemas import ReservationCreate
from core.models.model import async_session, ReservationsTable, UsersTable


class ReservationRepository:
    @classmethod
    async def add_one_reservation(cls, date: ReservationCreate) -> int:
        async with async_session() as session:
            reservation_dick = date.model_dump()

            reservation = ReservationsTable(**reservation_dick)
            session.add(reservation)
            await session.flush()
            await session.commit()
            return reservation.id

    @classmethod
    async def find_all_reservation(cls):
        async with async_session() as session:
            query = select(ReservationsTable)
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            return reservation_models

    @classmethod
    async def find_all_user(cls):
        async with async_session() as session:
            query = select(UsersTable)
            result = await session.execute(query)
            user_models = result.scalars().all()
            return user_models
