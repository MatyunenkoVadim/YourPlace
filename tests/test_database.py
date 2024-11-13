import unittest
from unittest.mock import patch
import asyncio

from app.database import (
    create_table,
    delete_tables,
    VisitorsTable,
    ReservationsTable,
    TablesTable,
    engine
)
from sqlalchemy import create_engine, text, insert
from datetime import datetime


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///test.db")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(create_table())

    def tearDown(self):
        self.loop.run_until_complete(delete_tables())
        self.loop.close()

    # Проверяет, что функция create_table создает все необходимые таблицы.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_create_table(self, mocked_engine):
        await create_table()

        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            table_names = [row[0] for row in result]
            self.assertIn("visitors", table_names)
            self.assertIn("reservation", table_names)
            self.assertIn("tables", table_names)

    # Проверяет, что функция delete_tables удаляет все таблицы.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_delete_tables(self, mocked_engine):
        await create_table()
        await delete_tables()

        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            table_names = [row[0] for row in result]
            self.assertNotIn("visitors", table_names)
            self.assertNotIn("reservation", table_names)
            self.assertNotIn("tables", table_names)

    # Проверяет, что можно добавить нового посетителя в таблицу VisitorsTable.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_add_visitor(self, mocked_engine):
        await create_table()

        async with engine.begin() as conn:
            await conn.execute(
                insert(VisitorsTable).values(
                    name="Иван Иванов",
                    phone="+79991234567"
                )
            )
            await conn.commit()

        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM visitors WHERE name = 'Иван Иванов' AND phone = '+79991234567'")
            )
            visitor = result.fetchone()
            self.assertIsNotNone(visitor)

    # Проверяет, что можно добавить новое бронирование в таблицу ReservationsTable.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_add_reservation(self, mocked_engine):
        await create_table()

        async with engine.begin() as conn:
            await conn.execute(
                insert(ReservationsTable).values(
                    guest_count=4,
                    reservation_date=datetime(2024, 1, 1, 12, 0, 0),
                    table_number="1"
                )
            )
            await conn.commit()

        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM reservation WHERE guest_count = 4 AND reservation_date = '2024-01-01 12:00:00' AND table_number = '1'")
            )
            reservation = result.fetchone()
            self.assertIsNotNone(reservation)

   # Проверяет, что можно добавить новый столик в таблицу TablesTable.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_add_table(self, mocked_engine):
        await create_table()

        async with engine.begin() as conn:
            await conn.execute(
                insert(TablesTable).values(
                    number_seats=6
                )
            )
            await conn.commit()

        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM tables WHERE number_seats = 6")
            )
            table = result.fetchone()
            self.assertIsNotNone(table)
