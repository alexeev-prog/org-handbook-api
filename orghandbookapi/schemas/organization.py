from pydantic import BaseModel


class PhoneNumberBase(BaseModel):
    """Схема валидации базовой модели номера телефона."""

    phone_number: str


class PhoneNumberCreate(PhoneNumberBase):
    """Схема валидации создания модели номера телефона."""


class PhoneNumber(PhoneNumberBase):
    """Схема валидации модели номера телефона."""

    id: int

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    """Схема валидации базовой модели организации."""

    legal_name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    """Схема валидации создания модели организации."""

    phone_numbers: list[str]
    activity_ids: list[int]


class OrganizationUpdate(BaseModel):
    """Схема валидации обновления модели организации."""

    legal_name: str | None = None
    building_id: int | None = None
    phone_numbers: list[str] | None = None
    activity_ids: list[int] | None = None


class Organization(OrganizationBase):
    """Схема валидации модели организации."""

    id: int

    class Config:
        from_attributes = True


class OrganizationWithRelations(Organization):
    """Схема валидации модели организации с отношениями."""  # noqa: RUF002

    building: "Building"
    phonenumbers: list[PhoneNumber]
    activities: list["Activity"]


from .activity import Activity  # noqa: E402
from .building import Building  # noqa: E402

OrganizationWithRelations.update_forward_refs()
