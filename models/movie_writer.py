from models.base import Base, Mapped, mapped_column
from sqlalchemy import ForeignKey

class MovieWriter(Base):
    __tablename__ = "movie_writer"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    writer_id: Mapped[int] = mapped_column(ForeignKey("writers.id"), primary_key=True)