import os
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException

from orghandbookapi.database.database import db_manager, url
from orghandbookapi.database.models.base import Base
from orghandbookapi.loader import config
from orghandbookapi.routers import api_router

current_dir = os.path.dirname(os.path.abspath(__file__))  # noqa: PTH100, PTH120
parent_dir = os.path.dirname(current_dir)  # noqa: PTH120


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция для жизненого цикла приложения."""
    db_manager.init(url)
    async with db_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await db_manager.close()


async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Верификация статичного токена API.

    Args:
        x_api_key (str, optional): Статичный токен для проверки.

    Raises:
        HTTPException: неверный API токен

    Returns:
        str: возвращает тот же API токен, если он верный.

    """
    if x_api_key != config.security.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


app = FastAPI(
    title="Org-Handbook-API",
    description="REST API для справочника организаций",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Маршрут для проверки работы API.

    Returns:
        dict[str, str]: ответ сервера

    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}  # noqa: DTZ003


app.include_router(
    api_router,
    dependencies=[Depends(verify_api_key)],
)


if __name__ == "__main__":
    uvicorn.run(
        "orghandbookapi.app:app",
        host=config.run.host,
        port=config.run.port,
        reload=False,
    )
