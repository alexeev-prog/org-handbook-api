from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.database import get_db_session
from orghandbookapi.database.models.repositories import BuildingRepository
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
    session: AsyncSession = Depends(get_db_session),
) -> list[Building]:
    buildings = await BuildingRepository.get_all(session)
    return buildings[skip : skip + limit]


@building_router.get("/{building_id}", response_model=BuildingWithRelations)
async def get_building(
    building_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> BuildingWithRelations:
    building = await BuildingRepository.get_with_relations(session, building_id)
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@building_router.post("/", response_model=Building)
async def create_building(
    building: BuildingCreate,
    session: AsyncSession = Depends(get_db_session),
) -> Building:
    return await BuildingRepository.create(session, building)


@building_router.put("/{building_id}", response_model=Building)
async def update_building(
    building_id: int,
    building: BuildingUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> Building:
    existing_building = await BuildingRepository.get(session, building_id)
    if not existing_building:
        raise HTTPException(status_code=404, detail="Building not found")

    return await BuildingRepository.update(session, building)


@building_router.delete("/{building_id}")
async def delete_building(
    building_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> dict[str, str]:
    await BuildingRepository.delete(session, building_id)
    return {"message": "Building deleted"}
