from typing import Optional

from pydantic import BaseModel

from orghandbookapi.database.models.organization import Organization


class ActivityBase(BaseModel):
    """Схема валидации базовой модели вида деятельности."""

    name: str
    parent_id: int | None = None
    level: int = 0


class ActivityCreate(ActivityBase):
    """Схема валидации создания модели вида деятельности."""


class ActivityUpdate(BaseModel):
    """Схема валидации обновления модели вида деятельности."""

    name: str | None = None
    parent_id: int | None = None
    level: int | None = None


class Activity(ActivityBase):
    """Схема валидации модели вида деятельности."""

    id: int

    class Config:
        from_attributes = True


class ActivityWithRelations(Activity):
    """Схема валидации модели вида деятельности с отношениями."""  # noqa: RUF002

    parent: Optional["Activity"] = None
    children: list["Activity"] = []
    organizations: list[Organization]


class ActivityTree(Activity):
    """Схема валидации дерева моделей видов деятельности."""

    children: list["ActivityTree"] = []


ActivityWithRelations.update_forward_refs()
ActivityTree.update_forward_refs()
