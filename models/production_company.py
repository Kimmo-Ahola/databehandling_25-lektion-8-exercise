from typing import List
from models.base import Base, str_255, Mapped, mapped_column, relationship

class ProductionCompany(Base):
    __tablename__ = "production_companies"

    name: Mapped[str_255] = mapped_column(primary_key=True)
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_production_company", back_populates="production_companies", init=False) # type: ignore