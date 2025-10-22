from sqlalchemy.orm import Mapped, mapped_column, relationship

from orghandbookapi.database.models.base import Base


class Building(Base):  # noqa: D101
    __tablename__ = "Buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    latitude: Mapped[float] = mapped_column(nullable=False)

    organizations: Mapped[list["Organization"]] = relationship(  # noqa: F821
        back_populates="building"
    )

    def __str__(self):  # noqa: D105
        return f"Building(id={self.id}, address={self.address!r})"

    def __repr__(self):  # noqa: D105
        return str(self)
