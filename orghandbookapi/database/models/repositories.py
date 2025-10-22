from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from orghandbookapi.database.models.activity import Activity
from orghandbookapi.database.models.base import Base
from orghandbookapi.database.models.building import Building
from orghandbookapi.database.models.organization import Organization


async def commit_process_session(
    session: AsyncSession, candidate: Any = None, flush: bool = False
):
    if flush:
        await session.flush()

    await session.commit()

    if candidate is not None:
        await session.refresh(candidate)


class CRUDRepository(ABC):
    @classmethod
    @abstractmethod
    async def get(cls, session: AsyncSession, id: int) -> Base | None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_with_relations(cls, session: AsyncSession, id: int) -> Base | None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def delete(cls, session: AsyncSession, id: int):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def update(cls, session: AsyncSession, model: BaseModel):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def create(cls, session: AsyncSession, model: BaseModel) -> Base:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_all(cls, session: AsyncSession) -> list[Base]:
        raise NotImplementedError


class OrganizationRepository(CRUDRepository):
    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Base | None:
        result = await session.execute(
            select(Organization).where(Organization.id == id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def get_with_relations(
        cls, session: AsyncSession, id: int
    ) -> Organization | None:
        result = await session.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phonenumbers),
                selectinload(Organization.activities),
            )
            .where(Organization.id == id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        organization = await cls.get(session, id)
        if organization:
            await session.delete(organization)
            await commit_process_session(session)

    @classmethod
    async def update(cls, session: AsyncSession, model: BaseModel):
        update_data = model.dict(exclude_unset=True)
        await session.execute(
            update(Organization)
            .where(Organization.id == update_data["id"])
            .values(**{k: v for k, v in update_data.items() if k != "id"})
        )
        await commit_process_session(session)

    @classmethod
    async def create(cls, session: AsyncSession, model: BaseModel) -> Organization:
        organization_data = model.dict()
        organization = Organization(**organization_data)
        session.add(organization)
        await commit_process_session(session, organization)
        return organization

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[Organization]:
        result = await session.execute(select(Organization))
        return result.scalars().all()

    @classmethod
    async def get_by_building(
        cls, session: AsyncSession, building_id: int
    ) -> list[Organization]:
        result = await session.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phonenumbers),
                selectinload(Organization.activities),
            )
            .where(Organization.building_id == building_id)
        )
        return result.scalars().all()

    @classmethod
    async def get_by_activity(
        cls, session: AsyncSession, activity_id: int
    ) -> list[Organization]:
        activities_cte = (
            select(Activity.id, Activity.parent_id, Activity.level)
            .where(Activity.id == activity_id)
            .cte(name="activities_cte", recursive=True)
        )

        recursive_select = (
            select(Activity.id, Activity.parent_id, Activity.level)
            .join(activities_cte, Activity.parent_id == activities_cte.c.id)
            .where(Activity.level < 3)
        )

        activities_cte = activities_cte.union_all(recursive_select)

        result = await session.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phonenumbers),
                selectinload(Organization.activities),
            )
            .join(Organization.activities)
            .where(Activity.id.in_(select(activities_cte.c.id)))
        )
        return result.scalars().all()

    @classmethod
    async def search_by_name(
        cls, session: AsyncSession, name: str
    ) -> list[Organization]:
        result = await session.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phonenumbers),
                selectinload(Organization.activities),
            )
            .where(Organization.name.ilike(f"%{name}%"))
        )
        return result.scalars().all()

    @classmethod
    async def get_in_radius(
        cls, session: AsyncSession, lat: float, lon: float, radius_km: float
    ) -> list[Organization]:
        distance = (
            func.acos(
                func.sin(func.radians(lat)) * func.sin(func.radians(Building.latitude))
                + func.cos(func.radians(lat))
                * func.cos(func.radians(Building.latitude))
                * func.cos(func.radians(Building.longitude) - func.radians(lon))
            )
            * 6371
        )

        result = await session.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phonenumbers),
                selectinload(Organization.activities),
            )
            .join(Organization.building)
            .where(distance <= radius_km)
        )
        return result.scalars().all()

    @classmethod
    async def get_in_rectangular_area(
        cls,
        session: AsyncSession,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
    ) -> list[Organization]:
        result = await session.execute(
            select(Organization)
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phonenumbers),
                selectinload(Organization.activities),
            )
            .join(Organization.building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon),
            )
        )
        return result.scalars().all()


class BuildingRepository(CRUDRepository):
    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Base | None:
        result = await session.execute(select(Building).where(Building.id == id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_with_relations(
        cls, session: AsyncSession, id: int
    ) -> Building | None:
        result = await session.execute(
            select(Building)
            .options(selectinload(Building.organizations))
            .where(Building.id == id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        building = await cls.get(session, id)
        if building:
            await session.delete(building)
            await commit_process_session(session)

    @classmethod
    async def update(cls, session: AsyncSession, model: BaseModel):
        update_data = model.dict(exclude_unset=True)
        await session.execute(
            update(Building)
            .where(Building.id == update_data["id"])
            .values(**{k: v for k, v in update_data.items() if k != "id"})
        )
        await commit_process_session(session)

    @classmethod
    async def create(cls, session: AsyncSession, model: BaseModel) -> Building:
        building_data = model.dict()
        building = Building(**building_data)
        session.add(building)
        await commit_process_session(session, building)
        return building

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[Building]:
        result = await session.execute(select(Building))
        return result.scalars().all()


class ActivityRepository(CRUDRepository):
    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Base | None:
        result = await session.execute(select(Activity).where(Activity.id == id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_with_relations(
        cls, session: AsyncSession, id: int
    ) -> Activity | None:
        result = await session.execute(
            select(Activity)
            .options(
                selectinload(Activity.parent),
                selectinload(Activity.children),
                selectinload(Activity.organizations),
            )
            .where(Activity.id == id)
        )
        return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, session: AsyncSession, id: int):
        activity = await cls.get(session, id)
        if activity:
            await session.delete(activity)
            await commit_process_session(session)

    @classmethod
    async def update(cls, session: AsyncSession, model: BaseModel):
        update_data = model.dict(exclude_unset=True)
        await session.execute(
            update(Activity)
            .where(Activity.id == update_data["id"])
            .values(**{k: v for k, v in update_data.items() if k != "id"})
        )
        await commit_process_session(session)

    @classmethod
    async def create(cls, session: AsyncSession, model: BaseModel) -> Activity:
        activity_data = model.dict()
        activity = Activity(**activity_data)
        session.add(activity)
        await commit_process_session(session, activity)
        return activity

    @classmethod
    async def get_all(cls, session: AsyncSession) -> list[Activity]:
        result = await session.execute(select(Activity))
        return result.scalars().all()

    @classmethod
    async def get_tree(
        cls, session: AsyncSession, parent_id: int | None = None
    ) -> list[Activity]:
        if parent_id is None:
            result = await session.execute(
                select(Activity).where(Activity.parent_id.is_(None))
            )
        else:
            result = await session.execute(
                select(Activity).where(Activity.parent_id == parent_id)
            )
        return result.scalars().all()
