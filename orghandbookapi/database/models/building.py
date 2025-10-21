from orghandbookapi.database.models.base import Base, int_pk
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Building(Base):
    __tablename__ = "Buildings"

    id: Mapped[int_pk]
    address: Mapped[str] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(  # noqa: F821
        "Organization", back_populates="building"
    )
