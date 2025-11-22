import json, random, os
from database.db import My_Session, engine
from models.actor import Actor
from models.base import Base
from models.cast import Cast
from models.director import Director
from models.genre import Genre
from models.movie import Movie
from models.production_company import ProductionCompany
from models.roletype import RoleType
from models.writer import Writer
from services.utils import Utils

class Seeding():
    @staticmethod
    def create_movie_database():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, "..", "datasets", "imdb.jsonl")
        file_path = os.path.normpath(file_path)

        # file_path = "datasets/imdb.jsonl" or use this version. Remember that the file path is relative to the main.py file

        uq_movies: set[str] = set() # the json file contains duplicates. 2 of each row. We use a set to filter out duplicates.
        roletypes = list(RoleType) # We fake role types as well, just to show that we can extend a bridge table with extra columns
        lower_bound, higher_bound = 1_000_000, 100_000_000 # We fake some salaries, this is not real data.

        with My_Session() as session:

            count = session.query(Movie).count()

            if count != 0: # We skip if there are already movies
                print("Movies are already seeded.")
                return

            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    data = json.loads(line)
                    url = data['url']

                    if url in uq_movies: # Skip duplicates. Each movie has a unique url
                        continue

                    uq_movies.add(url) # else add to the set to keep track

                    # mov = Movie(**data) # can only be used if we implement ALL keywords from the json file. 
                    # Currently the origin countries (many-to-many between movies and countries) is missing
                    # Needs to be optional because there are a lot of null values in countries.

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

                    # We read the data to our tables from the jsonl file
                    # the session keeps track of it all

                    # Check the utils file to see how it splits the full name into first and last names
                    # Also take a look at directors.py, actors.py to see the computed columns for full_name


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
                            first_name, last_name = Utils.split_full_name(d)                   
                            session.add(Director(first_name=first_name, last_name=last_name))
                        if director is not None:
                            movie.directors.append(director)

                    for w in data.get("writers", []):
                        writer = session.query(Writer).filter(Writer.full_name == w).first()
                        if writer is None:
                            first_name, last_name = Utils.split_full_name(w)                   
                            session.add(Writer(first_name=first_name, last_name=last_name))
                        if writer is not None:
                            movie.writers.append(writer)


                    for c in data.get("cast", []):
                        actor_name = c['actor']
                        role = c['role'] if c['role'] is not None else "Unknown"

                        first_name, last_name = Utils.split_full_name(actor_name)

                        actor = Actor(first_name=first_name, last_name=last_name)

                        movie.cast.append(Cast(actor=actor, role=role, role_type=random.choice(roletypes), salary=random.randrange(lower_bound, higher_bound)))

                session.commit()