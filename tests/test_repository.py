"""Тесты"""
import unittest
import asyncio

from datetime import datetime

from sqlalchemy import create_engine, text, select

from app.database import (
    engine,
    ReservationsTable,
    async_session,
    create_table,
)
from app.repository import ReservationRepository
from app.schemas import ReservationCreate


async def delete_reservations():
    """Удаляет все записи из таблицы 'reservation'."""
    async with engine.begin() as conn:
        await conn.execute(text("DELETE FROM reservation"))
        await conn.commit()


class TestReservationRepository(unittest.TestCase):
    """Тесты для репозитория бронирований."""

    def setUp(self):
        """Настройка тестовой базы данных перед каждым тестом."""
        self.engine = create_engine("sqlite+aiosqlite:///test.db")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(create_table())

    def tearDown(self):
        """Очистка тестовой базы данных после каждого теста."""
        self.loop.run_until_complete(delete_reservations())
        self.loop.close()

    def test_add_one(self):
        """Проверяет корректность данных при добавлении бронирования."""

        async def run_test():
            reservation = ReservationCreate(
                guest_count=2,
                reservation_date=datetime(2025, 1, 10, 12, 0, 0),
                table_number="1",
            )

            reservation_id = await ReservationRepository.add_one(reservation)

            async with async_session() as session:
                result = await session.execute(
                    select(ReservationsTable).where(
                        ReservationsTable.id == reservation_id
                    )
                )
                reservation_from_db = result.scalar_one_or_none()
                self.assertIsNotNone(reservation_from_db)
                self.assertEqual(
                    reservation_from_db.guest_count, reservation.guest_count
                )
                self.assertEqual(
                    reservation_from_db.reservation_date,
                    reservation.reservation_date,
                )
                self.assertEqual(
                    reservation_from_db.table_number, reservation.table_number
                )

        self.loop.run_until_complete(run_test())

    def test_find_all(self):
        """Проверяет, что метод find_all возвращает список всех бронирований."""

        async def run_test():
            reservation1 = ReservationCreate(
                guest_count=2,
                reservation_date=datetime(2025, 1, 5, 12, 0, 0),
                table_number="1",
            )
            reservation2 = ReservationCreate(
                guest_count=4,
                reservation_date=datetime(2025, 1, 15, 18, 0, 0),
                table_number="2",
            )

            await ReservationRepository.add_one(reservation1)
            await ReservationRepository.add_one(reservation2)

            reservations = await ReservationRepository.find_all()

            self.assertEqual(len(reservations), 2)

        self.loop.run_until_complete(run_test())

    def test_add_one_invalid_date(self):
        """Проверяет, что метод add_one выдает ошибку при некорректном формате даты."""

        async def run_test():
            reservation = ReservationCreate(
                guest_count=2,
                reservation_date="2025-01-01T12:00",  # Некорректный формат даты
                table_number="1",
            )
            with self.assertRaises(ValueError) as context:
                await ReservationRepository.add_one(reservation)
            self.assertTrue("invalid date format" in str(context.exception))

        self.loop.run_until_complete(run_test())

    def test_find_all_empty_table(self):
        """Проверяет, что метод find_all возвращает пустой список, если в таблице нет записей."""

        async def run_test():
            await delete_reservations()  # Очищаем таблицу перед тестом
            reservations = await ReservationRepository.find_all()
            self.assertEqual(reservations, [])

        self.loop.run_until_complete(run_test())

    def test_add_one_existing_table(self):
        """Проверяет, что метод add_one не добавляет новое бронирование,
        если столик уже забронирован на это время.
        """

        async def run_test():
            await ReservationRepository.add_one(
                ReservationCreate(
                    guest_count=2,
                    reservation_date=datetime(2025, 1, 20, 12, 0, 0),
                    table_number="1",
                )
            )

            with self.assertRaises(Exception) as context:
                await ReservationRepository.add_one(
                    ReservationCreate(
                        guest_count=2,
                        reservation_date=datetime(2025, 1, 20, 12, 0, 0),
                        table_number="1",
                    )
                )
            self.assertTrue("Этот столик уже забронирован" in str(context.exception))

            # Проверяем, что в базе данных только одно бронирование
            reservations = await ReservationRepository.find_all()
            self.assertEqual(len(reservations), 1)

        self.loop.run_until_complete(run_test())

    def test_add_one_negative_guest_count(self):
        """Проверяет, что метод add_one выдает ошибку при отрицательном количестве гостей."""

        async def run_test():
            with self.assertRaises(ValueError) as context:
                await ReservationRepository.add_one(
                    ReservationCreate(
                        guest_count=-2,
                        reservation_date=datetime(2025, 1, 25, 12, 0, 0),
                        table_number="1",
                    )
                )
            self.assertEqual(
                str(context.exception),
                "Количество гостей должно быть положительным числом",
            )

        self.loop.run_until_complete(run_test())

    def test_add_one_null_guest_count(self):
        """Проверяет, что метод add_one выдает ошибку при нулевом количестве гостей."""

        async def run_test():
            with self.assertRaises(ValueError) as context:
                await ReservationRepository.add_one(
                    ReservationCreate(
                        guest_count=0,
                        reservation_date=datetime(2025, 1, 25, 12, 0, 0),
                        table_number="1",
                    )
                )
            self.assertEqual(
                str(context.exception),
                "Количество гостей должно быть положительным числом",
            )

        self.loop.run_until_complete(run_test())
