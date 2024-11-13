"""Тесты маршрутов"""
from datetime import datetime

from unittest.mock import patch
import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import ReservationCreate


@pytest.mark.asyncio
async def test_reserve_table():
    """Проверяет успешное бронирование столика."""
    mock_add_one = patch("app.repository.ReservationRepository.add_one")
    mock_add_one.return_value = 1

    client = TestClient(app)
    response = client.post(
        "/result",
        data={
            "guest_count": "2",
            "reservation_date": "2025-01-01T12:00:00",
            "table_number": "1",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1}  # Проверка, что ответ содержит ID
    mock_add_one.assert_called_once_with(
        ReservationCreate(
            guest_count=2,
            reservation_date=datetime(2025, 1, 1, 12, 0, 0),
            table_number="1",
        )
    )


@pytest.mark.asyncio
async def test_reserve_table_invalid_date():
    """Проверяет обработку некорректного формата даты."""
    mock_add_one = patch("app.repository.ReservationRepository.add_one")
    mock_add_one.return_value = 1

    client = TestClient(app)
    response = client.post(
        "/result",
        data={
            "guest_count": "2",
            "reservation_date": "2025-01-01T12:00",  # Некорректный  формат  даты
            "table_number": "1",
        },
    )

    assert response.status_code == 400
    assert "Invalid reservation date format." in response.text
    mock_add_one.assert_not_called()


@pytest.mark.asyncio
async def test_select_guests():
    """Проверяет получение списка гостей."""
    client = TestClient(app)
    response = client.get("/guests")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_select_datetime():
    """Проверяет получение формы выбора даты."""
    client = TestClient(app)
    response = client.get("/datetime?guest_count=4")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_select_table_valid_date():
    """Проверяет получение списка столов для заданной даты."""
    client = TestClient(app)
    response = client.get(
        "/table_selection?guest_count=4&reservation_date=2025-01-01T19:00:00"
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_select_table_invalid_date():
    """Проверяет обработку некорректного формата даты при выборе столика."""
    client = TestClient(app)
    response = client.get("/table_selection?guest_count=4&reservation_date=2024-01-01")
    assert response.status_code == 400
    assert "Invalid date format." in response.text
