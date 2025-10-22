from typing import Optional

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id"), nullable=True
    )
    level: Mapped[int] = mapped_column(Integer, default=0)

    parent: Mapped[Optional["Activity"]] = relationship(
        remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")
    organizations: Mapped[list["Organization"]] = relationship(  # noqa: F821
        "Organization", back_populates="activities"
    )

    def __str__(self):
        return f"Activity(id={self.id}, name={self.name!r}, level={self.level})"

    def __repr__(self):
        return str(self)
