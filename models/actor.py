from typing import List, Optional
from sqlalchemy import Computed, String
from models.base import Base, int_pk, str_255, Mapped, mapped_column, relationship

class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int_pk] = mapped_column(init=False)
    first_name: Mapped[str_255]
    last_name: Mapped[Optional[str_255]]

    full_name: Mapped[str] = mapped_column(String(1000),
        Computed("CONCAT(IFNULL(first_name, ''), ' ', IFNULL(last_name, ''))"),
        init=False,
    )

    cast_roles: Mapped[List["Cast"]] = relationship(back_populates="actor", init=False) # type: ignore