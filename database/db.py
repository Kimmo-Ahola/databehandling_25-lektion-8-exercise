from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(url="mysql+pymysql://user:user123@localhost:3306/movie_db")

My_Session = sessionmaker(bind=engine)