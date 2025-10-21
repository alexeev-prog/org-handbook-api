import contextlib
from collections.abc import AsyncIterator
from typing import Optional

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from orghandbookapi.loader import config

url = config.database.url_format.format(
    host=config.database.host,
    port=config.database.port,
    name=config.database.name,
    user=config.database.user,
    password=config.database.password,
)

# url = "sqlite+aiosqlite:///data/sinwinapi.db"


class DatabaseSessionManager:
    """Менеджер сессий баз данных"""

    def __init__(self):
        """Инициализация класса"""
        # Движок, в данном случае - асинхронный
        self._engine: Optional[AsyncEngine] = None
        # Создатель сессий
        self._sessionmaker: Optional[async_sessionmaker[AsyncSession]] = None

    def init(self, db_url: str):
        """
        Инициализация сессий базы данных

        Args:
            db_url (str): путь до базы данных

        """
        if "postgresql" in db_url:
            connect_args = {
                "statement_cache_size": 0,
                "prepared_statement_cache_size": 0,
            }
        else:
            connect_args = {"check_same_thread": False}

        # Создание движка и создателя сессий

        self._engine = create_async_engine(
            url=db_url, pool_pre_ping=True, connect_args=connect_args
        )
        self._sessionmaker = async_sessionmaker(
            bind=self._engine, expire_on_commit=config.database.expire_on_commit
        )

    async def close(self):
        """Закрытие сессии базы данных"""
        if self._engine is None:
            return

        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """
        Контекстный менеджер сессии (позволяет получить доступ к ней)

        Raises:
            IOError: В случае если база данных не инициализирована

        Returns:
            AsyncIterator[AsyncSession]: асинхронный итератор

        Yields:
            Iterator[AsyncIterator[AsyncSession]]: асинхронный итератор сессии

        """
        if self._sessionmaker is None:
            raise OSError("DatabaseSessionManager is not initialized")

        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        Контекстный менеджер подключения

        Raises:
            IOError: база данных не инициализирована

        Returns:
            AsyncIterator[AsyncConnection]: асинхронный итератор

        Yields:
            Iterator[AsyncIterator[AsyncConnection]]: асинхронный итератор подключения

        """
        if self._engine is None:
            raise OSError("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise


db_manager = DatabaseSessionManager()
