from models.base import Base, str_255, Mapped, mapped_column
from sqlalchemy import ForeignKey

class MovieProductionCompany(Base):
    __tablename__ = "movie_production_company"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    company_name: Mapped[str_255] = mapped_column(ForeignKey("production_companies.name"), primary_key=True)