from sqlalchemy import Computed, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass, Session, relationship
import json
from typing import Annotated, List, Optional
from enum import Enum as PyEnum
import random

file_path = "dataset/imdb.jsonl"

str_255 = Annotated[str, mapped_column(String(255))]
int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class RoleType(PyEnum):
    LEADING = "Leading"
    SUPPORT = "Support"

class Cast(Base):
    __tablename__ = "cast"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True, init=False)
    actor_id: Mapped[int] = mapped_column(ForeignKey("actors.id"), primary_key=True, init=False)
    role: Mapped[str_255]
    salary: Mapped[float]
    role_type: Mapped[RoleType]

    actor: Mapped["Actor"] = relationship(back_populates="cast_roles")
    movie: Mapped["Movie"] = relationship(back_populates="cast", init=False)

class MovieDirection(Base):
    __tablename__ = "movie_direction"

    director_id: Mapped[int] = mapped_column(ForeignKey("directors.id"), primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)

class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str_255] = mapped_column(primary_key=True)
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_genre",
                                                 back_populates="genres", init=False)
    
class ProductionCompany(Base):
    __tablename__ = "production_companies"

    name: Mapped[str_255] = mapped_column(primary_key=True)
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_production_company", back_populates="production_companies", init=False)

class MovieProductionCompany(Base):
    __tablename__ = "movie_production_company"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    company_name: Mapped[str_255] = mapped_column(ForeignKey("production_companies.name"), primary_key=True)

class MovieGenres(Base):
    __tablename__ = "movie_genre"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    genre_name: Mapped[str] = mapped_column(ForeignKey("genres.name"), primary_key=True)

class Director(Base):
    __tablename__ = "directors"

    id: Mapped[int_pk] = mapped_column(init=False)

    first_name: Mapped[str_255]
    last_name: Mapped[Optional[str_255]]

    full_name: Mapped[str] = mapped_column(String(1000),
        Computed("CONCAT(IFNULL(first_name, ''), ' ', IFNULL(last_name, ''))"),
        init=False,
    )
    movies: Mapped[List["Movie"]] = relationship(secondary="movie_direction", back_populates="directors", init=False)

class Actor(Base):
    __tablename__ = "actors"

    id: Mapped[int_pk] = mapped_column(init=False)
    first_name: Mapped[str_255]
    last_name: Mapped[Optional[str_255]]

    cast_roles: Mapped[List["Cast"]] = relationship(back_populates="actor", init=False)

class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    url: Mapped[Optional[str_255]]
    name: Mapped[Optional[str_255]]
    score: Mapped[Optional[float]]
    top_rate: Mapped[Optional[str_255]]
    year: Mapped[Optional[int]]
    length: Mapped[Optional[str_255]]
    popularity: Mapped[Optional[str_255]]
    storyline: Mapped[Optional[str]] = mapped_column(Text)
    gross_worldwide: Mapped[Optional[str_255]]
    budget: Mapped[Optional[str_255]]
    origin_language: Mapped[Optional[str_255]]
    wins: Mapped[Optional[str_255]]
    nominations: Mapped[Optional[str_255]]


    genres: Mapped[List["Genre"]] = relationship(secondary="movie_genre", back_populates="movies", init=False)
    cast: Mapped[List[Cast]] = relationship(back_populates="movie", init=False)

    directors: Mapped[List["Director"]] = relationship(secondary="movie_direction", back_populates="movies", init=False)
    writers: Mapped[List["Writer"]] = relationship(secondary="movie_writer", back_populates="movies", init=False)

    production_companies: Mapped[List["ProductionCompany"]] = relationship(secondary="movie_production_company", back_populates="movies", init=False)

class MovieWriter(Base):
    __tablename__ = "movie_writer"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    writer_id: Mapped[int] = mapped_column(ForeignKey("writers.id"), primary_key=True)

class Writer(Base):
    __tablename__ = "writers"

    id: Mapped[int_pk] = mapped_column(init=False)

    first_name: Mapped[str_255]
    last_name: Mapped[Optional[str_255]]

    movies: Mapped[List["Movie"]] = relationship(secondary="movie_writer", back_populates="writers")

engine = create_engine("mysql+pymysql://kimmo:kimmo123@localhost:3306/movie_db")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

uq_movies: set[str] = set() # the json file contains duplicates. 2 of each row
roletypes = list(RoleType)
lower_bound, higher_bound = 1_000_000, 100_000_000

with Session(engine) as session:
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            url = data['url']

            if url in uq_movies:
                continue

            uq_movies.add(url)

            # mov = Movie(**data)

            movie = Movie(url=url, 
                          name=data['name'], 
                          score=data['score'], 
                          top_rate=data['top_rate'], 
                          year=data['year'], 
                          length=data['length'], 
                          popularity=data['popularity'], 
                          storyline=data['storyline'],
                          gross_worldwide=data['gross_worldwide'],
                          budget=data['budget'],
                          wins=data['wins'],
                          nominations=data['nominations'],
                          origin_language=data['origin_language']
                          )
            
            session.add(movie)

            for g in data.get("genres", []):
                genre = session.get(Genre, g)
                if genre is None:
                    session.add(Genre(name=g))
                if genre is not None:
                    movie.genres.append(genre)

            for pc in data.get("production_companies", []):
                production_company = session.get(ProductionCompany, pc)
                if production_company is None:
                    session.add(ProductionCompany(name=pc))
                if production_company is not None:
                    movie.production_companies.append(production_company)

            for d in data.get("directors", []):
                director = session.query(Director).filter(Director.full_name == d).first()
                if director is None:
                   split_name = d.split()
                   first_name = split_name[0]
                   last_name = split_name[1] if len(split_name) > 1 else ""
                   
                   session.add(Director(first_name=first_name, last_name=last_name))
                if director is not None:
                    movie.directors.append(director)


            for c in data.get("cast", []):
                actor_name = c['actor']
                role = c['role'] if c['role'] is not None else "Unknown"

                split_name = actor_name.split()

                first_name = split_name[0]
                last_name = split_name[1] if len(split_name) > 1 else ""
                
                actor = Actor(first_name=first_name, last_name=last_name)

                movie.cast.append(Cast(actor=actor, role=role, role_type=random.choice(roletypes), salary=random.randrange(lower_bound, higher_bound)))

        session.commit()