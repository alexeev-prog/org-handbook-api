from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.repositories import BuildingRepository
from orghandbookapi.schemas.building import (
    Building,
    BuildingCreate,
    BuildingUpdate,
    BuildingWithRelations,
)

building_router = APIRouter()


@building_router.get("/", response_model=list[Building])
async def get_buildings(
    skip: int = 0,
    limit: int = 100,
    session: FromDishka[AsyncSession] = Depends(),  # noqa: B008
) -> list[Building]:
    """
    Маршрут получения зданий.

    Args:
        skip (int, optional): пропуск.
        limit (int, optional): лимит.
        session (FromDishka[AsyncSession], optional): сессия бд.

    Returns:
        list[Building]: список зданий.

    """
    buildings = await BuildingRepository.get_all(session)
    return buildings[skip : skip + limit]


@building_router.get("/{building_id}", response_model=BuildingWithRelations)
async def get_building(
    building_id: int,
    session: FromDishka[AsyncSession] = Depends(),  # noqa: B008
) -> Building:
    """
    Маршрут получения здания.

    Args:
        building_id (int): ID здания.
        session (FromDishka[AsyncSession], optional): Сессия БД.

    Raises:
        HTTPException: здание не найдено.

    Returns:
        Building: здание.

    """
    building = await BuildingRepository.get_with_relations(session, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@building_router.post("/", response_model=Building)
async def create_building(
    building: BuildingCreate,
    session: FromDishka[AsyncSession] = Depends(),  # noqa: B008
) -> Building:
    """
    Мршраут создания модели здания.

    Args:
        building (BuildingCreate): Здание.
        session (FromDishka[AsyncSession], optional): Сессия БД.

    Returns:
        Building: Здание.

    """
    return await BuildingRepository.create(session, building)


@building_router.put("/{building_id}", response_model=Building)
async def update_building(
    building_id: int,
    building: BuildingUpdate,
    session: FromDishka[AsyncSession] = Depends(),  # noqa: B008
) -> Building:
    """
    Маршрут обновления здания.

    Args:
        building_id (int): ID здания.
        building (BuildingUpdate): здание.
        session (FromDishka[AsyncSession], optional): Сессия БД.

    Raises:
        HTTPException: здание не найдено.

    Returns:
        Building: Обновленное здание.

    """
    existing_building = await BuildingRepository.get(session, building_id)
    if not existing_building:
        raise HTTPException(status_code=404, detail="Building not found")

    return await BuildingRepository.update(session, building)


@building_router.delete("/{building_id}")
async def delete_building(
    building_id: int,
    session: FromDishka[AsyncSession] = Depends(),  # noqa: B008
) -> dict[str, str]:
    """
    Маршрут удаления здания.

    Args:
        building_id (int): ID здания.
        session (FromDishka[AsyncSession], optional): Сессия БД.

    Returns:
        dict[str, str]: ответ сервера

    """
    await BuildingRepository.delete(session, building_id)
    return {"message": "Building deleted"}
