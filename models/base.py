from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Integer
from typing import Annotated


str_255 = Annotated[str, mapped_column(String(255))]
int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

class Base(MappedAsDataclass, DeclarativeBase):
    pass