from typing import List, Optional
from sqlalchemy import Computed, String
from models import movie_direction
from models.base import Base, str_255, int_pk, Mapped, mapped_column, relationship

class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int_pk]

    first_name: Mapped[str_255]
    last_name: Mapped[Optional[str_255]]

    # https://dev.to/arctype/a-complete-guide-to-generated-columns-in-mysql-2lnb
    full_name: Mapped[str] = mapped_column(String(1000),
        Computed("CONCAT(IFNULL(first_name, ''), ' ', IFNULL(last_name, ''))")
    )
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_direction", back_populates="directors") # type: ignore
