"""Тесты"""
import pytest
from sqlalchemy import text, create_engine

from app.database import (
    create_table,
    delete_tables,
)

engine = create_engine("sqlite+aiosqlite:///test.db")


@pytest.mark.asyncio
async def test_create_table():
    """Проверяет успешное создание таблиц в базе данных."""
    await create_table()

    # Проверка, что таблицы созданы
    result = engine.connect().execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    )
    table_names = [row[0] for row in result]
    assert "visitors" in table_names
    assert "reservation" in table_names
    assert "tables" in table_names


@pytest.mark.asyncio
async def test_delete_tables():
    """Проверяет успешное удаление таблиц из базы данных."""
    await create_table()  # Сначала создаем таблицы
    await delete_tables()

    # Проверка, что таблицы удалены
    result = engine.connect().execute(
        text("SELECT name FROM sqlite_master WHERE type='table'")
    )
    table_names = [row[0] for row in result]
    assert "visitors" not in table_names
    assert "reservation" not in table_names
    assert "tables" not in table_names
