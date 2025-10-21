from typing import List, Optional

from pydantic import BaseModel

from orghandbookapi.database.models.organization import Organization


class BuildingBase(BaseModel):
    address: str
    longitude: float
    latitude: float


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BaseModel):
    address: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None


class Building(BuildingBase):
    id: int

    class Config:
        from_attributes = True


class BuildingWithRelations(Building):
    organizations: List[Organization]
