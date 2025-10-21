from typing import List, Optional

from pydantic import BaseModel

from orghandbookapi.database.models.activity import Activity
from orghandbookapi.database.models.building import Building


class PhoneNumberBase(BaseModel):
    phone_number: str


class PhoneNumberCreate(PhoneNumberBase):
    pass


class PhoneNumber(PhoneNumberBase):
    id: int

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    legal_name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    phone_numbers: List[str]
    activity_ids: List[int]


class OrganizationUpdate(BaseModel):
    legal_name: Optional[str] = None
    building_id: Optional[int] = None
    phone_numbers: Optional[List[str]] = None
    activity_ids: Optional[List[int]] = None


class Organization(OrganizationBase):
    id: int
    building: Building
    phonenumbers: List[PhoneNumber]
    activities: List[Activity]

    class Config:
        from_attributes = True


class OrganizationWithRelations(Organization):
    building: Building
    phonenumbers: List[PhoneNumber]
    activities: List[Activity]
