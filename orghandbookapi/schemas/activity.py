from typing import List, Optional

from pydantic import BaseModel

from orghandbookapi.database.models.organization import Organization


class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    level: int = 0


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    level: Optional[int] = None


class Activity(ActivityBase):
    id: int

    class Config:
        from_attributes = True


class ActivityWithRelations(Activity):
    parent: Optional["Activity"] = None
    children: List["Activity"] = []
    organizations: List[Organization]


class ActivityTree(Activity):
    children: List["ActivityTree"] = []


ActivityWithRelations.update_forward_refs()
ActivityTree.update_forward_refs()
