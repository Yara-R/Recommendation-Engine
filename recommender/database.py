from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from recommender.settings import Settings

engine = create_engine(Settings().DATABASE_URL)

Base = declarative_base()


def get_session():
    with Session(engine) as session:
        yield session
