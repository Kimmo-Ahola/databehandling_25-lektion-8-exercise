from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import MetaData, String, Integer
from typing import Annotated


str_255 = Annotated[str, mapped_column(String(255))]
int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

class Base(MappedAsDataclass, DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })