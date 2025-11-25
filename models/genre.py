from typing import List
from models.base import Base, str_255, Mapped, mapped_column, relationship

class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str_255] = mapped_column(primary_key=True)
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_genre", back_populates="genres") # type: ignore