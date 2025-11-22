from models.base import Base, Mapped, mapped_column
from sqlalchemy import ForeignKey

class MovieDirection(Base):
    __tablename__ = "movie_direction"

    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)