from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orghandbookapi.database.models.base import Base

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column(
        "organization_id", Integer, ForeignKey("Organizations.id"), primary_key=True
    ),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True),
)


class Organization(Base):  # noqa: D101
    __tablename__ = "Organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    legal_name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("Buildings.id"), nullable=False)

    building: Mapped["Building"] = relationship(back_populates="organizations")  # noqa: F821
    phonenumbers: Mapped[list["PhoneNumber"]] = relationship(
        back_populates="organization", cascade="all, delete-orphan"
    )
    activities: Mapped[list["Activity"]] = relationship(  # noqa: F821
        secondary=organization_activity, back_populates="organizations", lazy="selectin"
    )

    def __str__(self):  # noqa: D105
        return f"Organization(id={self.id}, name={self.legal_name!r})"

    def __repr__(self):  # noqa: D105
        return str(self)


class PhoneNumber(Base):  # noqa: D101
    __tablename__ = "OrgPhoneNumbers"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("Organizations.id"), nullable=False
    )

    organization: Mapped["Organization"] = relationship(back_populates="phonenumbers")

    def __str__(self):  # noqa: D105
        return f"PhoneNumber(id={self.id}, number={self.phone_number!r})"

    def __repr__(self):  # noqa: D105
        return str(self)
