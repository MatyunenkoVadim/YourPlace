from sqlalchemy import select

from schemas import ReservationCreate
from database import async_session, ReservationsTable


class ReservationRepository:
    @classmethod
    async def add_one(cls, date: ReservationCreate) -> int:
        async with async_session() as session:
            reservation_dick = date.model_dump()

            reservation = ReservationsTable(**reservation_dick)
            session.add(reservation)
            await session.flush()
            await session.commit()
            return reservation.id

    @classmethod
    async def find_all(cls):
        async with async_session() as session:
            query = select(ReservationsTable)
            result = await session.execute(query)
            reservation_models = result.scalars().all()
            return reservation_models