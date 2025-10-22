from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.database import get_db_session
from orghandbookapi.database.models.repositories import ActivityRepository
from orghandbookapi.schemas.activity import (
    Activity,
    ActivityCreate,
    ActivityTree,
    ActivityUpdate,
    ActivityWithRelations,
)

activity_router = APIRouter()


@activity_router.get("/", response_model=list[Activity])
async def get_activities(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_db_session),
):
    activities = await ActivityRepository.get_all(session)
    return activities[skip : skip + limit]


@activity_router.get("/{activity_id}", response_model=ActivityWithRelations)
async def get_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    activity = await ActivityRepository.get_with_relations(session, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@activity_router.post("/", response_model=Activity)
async def create_activity(
    activity: ActivityCreate,
    session: AsyncSession = Depends(get_db_session),
):
    return await ActivityRepository.create(session, activity)


@activity_router.put("/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: int,
    activity: ActivityUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    existing_activity = await ActivityRepository.get(session, activity_id)
    if not existing_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    return await ActivityRepository.update(session, activity)


@activity_router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    await ActivityRepository.delete(session, activity_id)
    return {"message": "Activity deleted"}


@activity_router.get("/tree/{parent_id}", response_model=list[ActivityTree])
async def get_activity_tree(
    parent_id: int | None = None,
    session: AsyncSession = Depends(get_db_session),
):
    return await ActivityRepository.get_tree(session, parent_id)
