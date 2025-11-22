from models.base import Base, Mapped, mapped_column
from sqlalchemy import ForeignKey

class MovieGenres(Base):
    __tablename__ = "movie_genre"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    genre_name: Mapped[str] = mapped_column(ForeignKey("genres.name"), primary_key=True)