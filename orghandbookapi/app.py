import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException

from orghandbookapi.database.database import db_manager, url
from orghandbookapi.database.models.base import Base
from orghandbookapi.loader import config
from orghandbookapi.routers import api_router

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_manager.init(url)
    async with db_manager.connect() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
    await db_manager.close()


app = FastAPI(
    title="Org-Handbook-API",
    description="REST API для справочника организаций",
    version="1.0.0",
    lifespan=lifespan,
)


async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != config.security.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Подключение роутеров
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
