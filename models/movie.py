from typing import List, Optional
from sqlalchemy import Text
from models import movie_direction
from models import movie_genres
from models import movie_writer
from models import movie_production_company
from models.base import Base, str_255, int_pk, Mapped, mapped_column, relationship

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int_pk] = mapped_column(init=False)
    url: Mapped[Optional[str_255]]
    name: Mapped[Optional[str_255]] = mapped_column(name='title')
    score: Mapped[Optional[float]]
    top_rate: Mapped[Optional[str_255]]
    year: Mapped[Optional[int]] = mapped_column(name='release_year')
    length: Mapped[Optional[str_255]] = mapped_column(name='duration')
    popularity: Mapped[Optional[str_255]]
    storyline: Mapped[Optional[str]] = mapped_column(Text)
    gross_worldwide: Mapped[Optional[str_255]]
    budget: Mapped[Optional[str_255]]
    origin_language: Mapped[Optional[str_255]]
    wins: Mapped[Optional[str_255]]
    nominations: Mapped[Optional[str_255]]

    # relationships are here
    genres: Mapped[List["Genre"]] = relationship(secondary="movie_genre", back_populates="movies", init=False) # type: ignore
    cast: Mapped[List["Cast"]] = relationship(back_populates="movie", init=False) # type: ignore

    directors: Mapped[List["Director"]] = relationship(secondary="movie_direction", back_populates="movies", init=False) # type: ignore
    writers: Mapped[List["Writer"]] = relationship(secondary="movie_writer", back_populates="movies", init=False) # type: ignore

    production_companies: Mapped[List["ProductionCompany"]] = relationship(secondary="movie_production_company", back_populates="movies", init=False) # type: ignore