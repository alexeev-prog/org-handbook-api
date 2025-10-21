from sqlalchemy import Integer, MetaData, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


str_uniq = Mapped[str] = mapped_column(String, unique=True, index=True)
str_pk = Mapped[int] = mapped_column(Integer, primary_key=True)
int_pk = Mapped[int] = mapped_column(Integer, primary_key=True)
str_null_true = Mapped[str | None] = mapped_column(String, nullable=True)
