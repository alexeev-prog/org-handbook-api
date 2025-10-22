from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.database import db_manager


class DatabaseProvider(Provider):
    """Провайдер базы данных (DI)."""

    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncSession:
        """Получение сессии базы данных."""
        async with db_manager.session() as session:
            yield session
