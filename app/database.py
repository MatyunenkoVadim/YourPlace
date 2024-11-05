from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

#DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/YourPlace"
# пока так, сами создавайте у себя бд, по-другому пока не придумала

engine = create_async_engine(
    "sqlite+aiosqlite:///YourPlace.db"
)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

class Model(DeclarativeBase):
    pass

class VisitorsTable(Model):
    __tablename__ = "visitors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    phone: Mapped[str]


class ReservationsTable(Model):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True)
    guest_count: Mapped[int]
    reservation_date: Mapped[datetime]
    table_number: Mapped[str]

class TablesTable(Model):
    __tablename__ = "tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    number_seats: Mapped[int]

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

# async def get_async_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
