from pydantic import BaseModel


class BuildingBase(BaseModel):
    """Схема валидации базовой модели здания."""

    address: str
    longitude: float
    latitude: float


class BuildingCreate(BuildingBase):
    """Схема валидации создания модели здания."""


class BuildingUpdate(BaseModel):
    """Схема валидации обновления модели здания."""

    address: str | None = None
    longitude: float | None = None
    latitude: float | None = None


class Building(BuildingBase):
    """Схема валидации модели здания."""

    id: int

    class Config:
        from_attributes = True


class BuildingWithRelations(Building):
    """Схема валидации модели здания с отношениями."""  # noqa: RUF002

    organizations: list["Organization"] = []


from .organization import Organization  # noqa: E402

BuildingWithRelations.update_forward_refs()
