from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.database import db_manager


class DatabaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_session(self) -> AsyncSession:
        async with db_manager.session() as session:
            yield session
