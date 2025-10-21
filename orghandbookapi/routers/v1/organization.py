from fastapi import APIRouter, Depends, HTTPException, Query
from dishka.integrations.fastapi import FromDishka
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from orghandbookapi.database.repositories import OrganizationRepository
from orghandbookapi.schemas.organization import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationWithRelations,
)

organizations_router = APIRouter()


@organizations_router.get("/", response_model=List[Organization])
async def get_organizations(
    skip: int = 0, limit: int = 100, session: FromDishka[AsyncSession] = Depends()
):
    organizations = await OrganizationRepository.get_all(session)
    return organizations[skip : skip + limit]


@organizations_router.get(
    "/{organization_id}", response_model=OrganizationWithRelations
)
async def get_organization(
    organization_id: int, session: FromDishka[AsyncSession] = Depends()
):
    organization = await OrganizationRepository.get_with_relations(
        session, organization_id
    )
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization


@organizations_router.post("/", response_model=Organization)
async def create_organization(
    organization: OrganizationCreate, session: FromDishka[AsyncSession] = Depends()
):
    return await OrganizationRepository.create(session, organization)


@organizations_router.put("/{organization_id}", response_model=Organization)
async def update_organization(
    organization_id: int,
    organization: OrganizationUpdate,
    session: FromDishka[AsyncSession] = Depends(),
):
    existing_org = await OrganizationRepository.get(session, organization_id)
    if not existing_org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return await OrganizationRepository.update(session, organization)


@organizations_router.delete("/{organization_id}")
async def delete_organization(
    organization_id: int, session: FromDishka[AsyncSession] = Depends()
):
    await OrganizationRepository.delete(session, organization_id)
    return {"message": "Organization deleted"}


@organizations_router.get(
    "/building/{building_id}", response_model=List[OrganizationWithRelations]
)
async def get_organizations_by_building(
    building_id: int, session: FromDishka[AsyncSession] = Depends()
):
    return await OrganizationRepository.get_by_building(session, building_id)


@organizations_router.get(
    "/activity/{activity_id}", response_model=List[OrganizationWithRelations]
)
async def get_organizations_by_activity(
    activity_id: int, session: FromDishka[AsyncSession] = Depends()
):
    return await OrganizationRepository.get_by_activity(session, activity_id)


@organizations_router.get(
    "/search/name", response_model=List[OrganizationWithRelations]
)
async def search_organizations_by_name(
    name: str = Query(..., min_length=1), session: FromDishka[AsyncSession] = Depends()
):
    return await OrganizationRepository.search_by_name(session, name)


@organizations_router.get(
    "/search/radius", response_model=List[OrganizationWithRelations]
)
async def get_organizations_in_radius(
    lat: float = Query(...),
    lon: float = Query(...),
    radius_km: float = Query(..., gt=0),
    session: FromDishka[AsyncSession] = Depends(),
):
    return await OrganizationRepository.get_in_radius(session, lat, lon, radius_km)


@organizations_router.get(
    "/search/area", response_model=List[OrganizationWithRelations]
)
async def get_organizations_in_rectangular_area(
    min_lat: float = Query(...),
    max_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lon: float = Query(...),
    session: FromDishka[AsyncSession] = Depends(),
):
    return await OrganizationRepository.get_in_rectangular_area(
        session, min_lat, max_lat, min_lon, max_lon
    )
