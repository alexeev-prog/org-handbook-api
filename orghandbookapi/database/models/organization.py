from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from orghandbookapi.database.models.activity import Activity
from orghandbookapi.database.models.base import Base, int_pk
from orghandbookapi.database.models.building import Building


class Organization(Base):
    __tablename__ = "Organizations"

    id: Mapped[int_pk]
    legal_name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey("building.id"), nullable=False)

    building: Mapped["Building"] = relationship(
        "Building", back_populates="organizations"
    )

    phonenumbers: Mapped[list["PhoneNumber"]] = relationship(
        "PhoneNumber", back_populates="organizations"
    )
    activities: Mapped[list["Activity"]] = relationship(
        "Activity", back_populates="organizations"
    )

    def __str__(self):
        return f"Organization(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return str(self)


class PhoneNumber(Base):
    __tablename__ = "OrgPhoneNumbers"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone_number: Mapped[str] = mapped_column(nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization", back_populates="phonenumbers"
    )
