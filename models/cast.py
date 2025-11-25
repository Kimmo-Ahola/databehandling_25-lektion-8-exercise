from models.base import Base, str_255, mapped_column, Mapped, relationship
from models.roletype import RoleType
from sqlalchemy import ForeignKey

class Cast(Base):
    __tablename__ = "cast"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.id"), primary_key=True)
    role: Mapped[str_255]
    salary: Mapped[float]
    role_type: Mapped[RoleType]

    actor: Mapped["Actor"] = relationship(back_populates="cast_roles") # type: ignore
    movie: Mapped["Movie"] = relationship(back_populates="cast") # type: ignore