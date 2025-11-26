from database.db import My_Session
from models.actor import Actor
from services.seeding import Seeding
from sqlalchemy.orm import Session

"""
Check the readme.md file for exercises

You can remove 
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
from the seeding class and use alembic if you want.

Write the questions as functions like below (or create a console menu)
"""

def Q_1(session: Session) -> Actor | None:
    query = session.query(Actor)

    res = query.first()

    return res


if __name__ == '__main__':
    Seeding.create_movie_database()
    
    with My_Session() as session:
        res = Q_1(session)
        if res:
            print(res.full_name)