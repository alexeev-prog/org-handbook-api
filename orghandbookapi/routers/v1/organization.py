from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.database import get_db_session
from orghandbookapi.database.models.repositories import OrganizationRepository
from orghandbookapi.schemas.organization import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationWithRelations,
)

organizations_router = APIRouter()


@organizations_router.get("/", response_model=list[Organization])
async def get_organizations(  # noqa: D103
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> list[Organization]:
    organizations = await OrganizationRepository.get_all(session)
    return organizations[skip : skip + limit]


@organizations_router.get(
    "/{organization_id}", response_model=OrganizationWithRelations
)
async def get_organization(  # noqa: D103
    organization_id: int,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> OrganizationWithRelations:
    organization = await OrganizationRepository.get_with_relations(
        session, organization_id
    )
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    return organization


@organizations_router.post("/", response_model=Organization)
async def create_organization(  # noqa: D103
    organization: OrganizationCreate,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> Organization:
    return await OrganizationRepository.create(session, organization)


@organizations_router.put("/{organization_id}", response_model=Organization)
async def update_organization(  # noqa: D103
    organization_id: int,
    organization: OrganizationUpdate,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> Organization:
    existing_org = await OrganizationRepository.get(session, organization_id)
    if not existing_org:
        raise HTTPException(status_code=404, detail="Organization not found")

    return await OrganizationRepository.update(session, organization)


@organizations_router.delete("/{organization_id}")
async def delete_organization(  # noqa: D103
    organization_id: int,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> dict[str, str]:
    await OrganizationRepository.delete(session, organization_id)
    return {"message": "Organization deleted"}


@organizations_router.get(
    "/building/{building_id}", response_model=list[OrganizationWithRelations]
)
async def get_organizations_by_building(  # noqa: D103
    building_id: int,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> list[OrganizationWithRelations]:
    return await OrganizationRepository.get_by_building(session, building_id)


@organizations_router.get(
    "/activity/{activity_id}", response_model=list[OrganizationWithRelations]
)
async def get_organizations_by_activity(  # noqa: D103
    activity_id: int,
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> list[OrganizationWithRelations]:
    return await OrganizationRepository.get_by_activity(session, activity_id)


@organizations_router.get(
    "/search/name", response_model=list[OrganizationWithRelations]
)
async def search_organizations_by_name(  # noqa: D103
    name: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> list[OrganizationWithRelations]:
    return await OrganizationRepository.search_by_name(session, name)


@organizations_router.get(
    "/search/radius", response_model=list[OrganizationWithRelations]
)
async def get_organizations_in_radius(  # noqa: D103
    lat: float = Query(...),
    lon: float = Query(...),
    radius_km: float = Query(..., gt=0),
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> list[OrganizationWithRelations]:
    return await OrganizationRepository.get_in_radius(session, lat, lon, radius_km)


@organizations_router.get(
    "/search/area", response_model=list[OrganizationWithRelations]
)
async def get_organizations_in_rectangular_area(  # noqa: D103
    min_lat: float = Query(...),
    max_lat: float = Query(...),
    min_lon: float = Query(...),
    max_lon: float = Query(...),
    session: AsyncSession = Depends(get_db_session),  # noqa: B008
) -> list[OrganizationWithRelations]:
    return await OrganizationRepository.get_in_rectangular_area(
        session, min_lat, max_lat, min_lon, max_lon
    )
