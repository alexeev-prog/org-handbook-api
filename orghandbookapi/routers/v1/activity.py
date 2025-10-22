from dishka.integrations.fastapi import FromDishka
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from orghandbookapi.database.repositories import ActivityRepository
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
    skip: int = 0, limit: int = 100, session: FromDishka[AsyncSession] = Depends()
):
    activities = await ActivityRepository.get_all(session)
    return activities[skip : skip + limit]


@activity_router.get("/{activity_id}", response_model=ActivityWithRelations)
async def get_activity(activity_id: int, session: FromDishka[AsyncSession] = Depends()):
    activity = await ActivityRepository.get_with_relations(session, activity_id)
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


@activity_router.post("/", response_model=Activity)
async def create_activity(
    activity: ActivityCreate, session: FromDishka[AsyncSession] = Depends()
):
    return await ActivityRepository.create(session, activity)


@activity_router.put("/{activity_id}", response_model=Activity)
async def update_activity(
    activity_id: int,
    activity: ActivityUpdate,
    session: FromDishka[AsyncSession] = Depends(),
):
    existing_activity = await ActivityRepository.get(session, activity_id)
    if not existing_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    return await ActivityRepository.update(session, activity)


@activity_router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int, session: FromDishka[AsyncSession] = Depends()
):
    await ActivityRepository.delete(session, activity_id)
    return {"message": "Activity deleted"}


@activity_router.get("/tree/{parent_id}", response_model=list[ActivityTree])
async def get_activity_tree(
    parent_id: int | None = None, session: FromDishka[AsyncSession] = Depends()
):
    return await ActivityRepository.get_tree(session, parent_id)
