import unittest
from datetime import datetime
from unittest.mock import patch
import asyncio

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import ReservationCreate


class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    @patch('app.repository.ReservationRepository.add_one')
    async def test_reserve_table(self, mock_add_one):
        mock_add_one.return_value = 1  # Симулируем  успешное  добавление  бронирования

        response = self.client.post(
            "/result",
            data={
                "guest_count": "2",
                "reservation_date": "2024-01-01T12:00:00",
                "table_number": "1"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Reservation made:", response.text)
        self.assertIn("2 guests", response.text)
        self.assertIn("2024-01-01 12:00:00", response.text)
        self.assertIn("Table 1", response.text)
        mock_add_one.assert_called_once_with(ReservationCreate(
            guest_count=2,
            reservation_date=datetime(2024, 1, 1, 12, 0, 0),
            table_number="1"
        ))

    @patch('app.repository.ReservationRepository.add_one')
    async def test_reserve_table_invalid_date(self, mock_add_one):
        mock_add_one.return_value = 1  # Симулируем  успешное  добавление  бронирования

        response = self.client.post(
            "/result",
            data={
                "guest_count": "2",
                "reservation_date": "2024-01-01T12:00",  # Некорректный  формат  даты
                "table_number": "1"
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid reservation date format.", response.text)
        mock_add_one.assert_not_called()