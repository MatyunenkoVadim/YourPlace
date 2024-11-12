import unittest
from unittest.mock import patch
import asyncio

from app.database import (
    create_table,
    delete_tables,
)
from sqlalchemy import create_engine, text


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///test.db")
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.run_until_complete(delete_tables())
        self.loop.close()

    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_create_table(self, mocked_engine):
        await create_table()

        # Проверка наличия таблиц
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            table_names = [row[0] for row in result]
            self.assertIn("visitors", table_names)
            self.assertIn("reservation", table_names)
            self.assertIn("tables", table_names)

    @patch('app.database.engine', new_callable=lambda: self.engine)
    async def test_delete_tables(self, mocked_engine):
        await create_table()
        await delete_tables()

        # Проверка удаления таблиц
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            table_names = [row[0] for row in result]
            self.assertNotIn("visitors", table_names)
            self.assertNotIn("reservation", table_names)
            self.assertNotIn("tables", table_names)