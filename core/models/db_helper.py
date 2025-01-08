"""
Этот модуль предоставляет вспомогательные функции для работы с базой данных,
используя SQLAlchemy и асинхронные сессии.

Классы:
- DatabaseHelper: Класс, который управляет созданием и конфигурацией асинхронных сессий базы данных.

Зависимости:
- Использует SQLAlchemy для работы с базой данных.
- Использует настройки из core.config для конфигурации подключения к базе данных.

Контекст:
Этот файл является частью системы управления базой данных и используется для
управления асинхронными сессиями и подключениями.
"""

from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from core.config import settings


class DatabaseHelper:
    """
    Класс, который управляет созданием и конфигурацией асинхронных сессий базы данных.
    """

    def __init__(self, url: str, echo: bool = False):
        """
        Инициализирует DatabaseHelper с заданным URL базы данных и параметром echo.

        Параметры:
        - url: URL для подключения к базе данных.
        - echo: Если True, SQLAlchemy будет выводить все SQL-запросы в консоль.
        """
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    def get_scoped_session(self):
        """
        Возвращает асинхронную сессию, привязанную к текущей задаче.

        Возвращает:
        - Асинхронная сессия, привязанная к текущей задаче.
        """
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        Асинхронный генератор, который предоставляет сессию для использования в FastAPI зависимостях.

        Возвращает:
        - Асинхронная сессия.
        """
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        """
        Асинхронный генератор, который предоставляет сессию, привязанную к текущей задаче,
        для использования в FastAPI зависимостях.

        Возвращает:
        - Асинхронная сессия, привязанная к текущей задаче.
        """
        session = self.get_scoped_session()
        yield session
        await session.close()

    async def dispose(self) -> None:
        """
        Закрывает все соединения и освобождает ресурсы, связанные с движком базы данных.
        """
        await self.engine.dispose()


db_helper = DatabaseHelper(
    url=settings.db_setting.db_url,
    echo=settings.db_setting.db_echo,
)
