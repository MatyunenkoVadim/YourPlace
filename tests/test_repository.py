import unittest
import asyncio
from unittest.mock import patch

from app.repository import ReservationRepository
from app.schemas import ReservationCreate
from app.database import engine, ReservationsTable, async_session, create_table
from sqlalchemy import create_engine, text, select
from datetime import datetime

class TestReservationRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///test.db")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(create_table())

    def tearDown(self):
        self.loop.run_until_complete(self.delete_reservations())
        self.loop.close()

    async def delete_reservations(self):
        async with engine.begin() as conn:
            await conn.execute(text("DELETE FROM reservation"))
            await conn.commit()

    # Проверяет корректность данных при добавлении бронирования
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_add_one(self, mocked_engine):
        reservation = ReservationCreate(
            guest_count=2,
            reservation_date=datetime(2024, 1, 1, 12, 0, 0),
            table_number="1"
        )

        reservation_id = await ReservationRepository.add_one(reservation)

        async with async_session() as session:
            result = await session.execute(select(ReservationsTable).where(ReservationsTable.id == reservation_id))
            reservation_from_db = result.scalar_one_or_none()
            self.assertIsNotNone(reservation_from_db)
            self.assertEqual(reservation_from_db.guest_count, reservation.guest_count)
            self.assertEqual(reservation_from_db.reservation_date, reservation.reservation_date)
            self.assertEqual(reservation_from_db.table_number, reservation.table_number)

    #Проверяет, что метод find_all возвращает список всех бронирований.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_find_all(self, mocked_engine):
        reservation1 = ReservationCreate(
            guest_count=2,
            reservation_date=datetime(2024, 1, 1, 12, 0, 0),
            table_number="1"
        )
        reservation2 = ReservationCreate(
            guest_count=4,
            reservation_date=datetime(2024, 1, 2, 18, 0, 0),
            table_number="2"
        )

        await ReservationRepository.add_one(reservation1)
        await ReservationRepository.add_one(reservation2)

        reservations = await ReservationRepository.find_all()

        self.assertEqual(len(reservations), 2)
        self.assertIn(reservation1.model_dump(), [r.model_dump() for r in reservations])
        self.assertIn(reservation2.model_dump(), [r.model_dump() for r in reservations])

    # Проверяет, что метод add_one выдает ошибку при некорректном формате даты.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_add_one_invalid_date(self, mocked_engine):
        reservation = ReservationCreate(
            guest_count=2,
            reservation_date="2024-01-01T12:00",  # Некорректный формат даты
            table_number="1"
        )
        with self.assertRaises(Exception) as context:
            await ReservationRepository.add_one(reservation)
        self.assertTrue('invalid date format' in str(context.exception))

    # Проверяет, что метод find_all возвращает пустой список, если в таблице нет записей.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_find_all_empty_table(self, mocked_engine):
        await create_table()
        reservations = await ReservationRepository.find_all()
        self.assertEqual(reservations, [])

    # Проверяет, что метод add_one не добавляет новое бронирование, если столик уже забронирован на это время.
    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_add_one_existing_table(self, mocked_engine):
        await create_table()

        await ReservationRepository.add_one(ReservationCreate(
            guest_count=2,
            reservation_date=datetime(2024, 1, 1, 12, 0, 0),
            table_number="1"
        ))

        with self.assertRaises(Exception) as context:
            await ReservationRepository.add_one(ReservationCreate(
                guest_count=2,
                reservation_date=datetime(2024, 1, 1, 12, 0, 0),
                table_number="1"
            ))
        self.assertTrue('table is already booked' in str(context.exception))