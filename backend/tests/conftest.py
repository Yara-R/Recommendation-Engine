from contextlib import contextmanager
from datetime import date, datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from recommender.app import app
from recommender.database import get_session
from recommender.models import Movie, User, table_registry


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        yield _engine


@pytest.fixture
def session(engine):
    # Cria as tabelas antes do teste
    table_registry.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Limpa as tabelas após o teste (opcional)
        table_registry.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    user = User(
        age=30,
        gender='M',
        uuid=uuid4(),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def movie(session):
    filme = Movie(
        title='Inception', genres='Sci-Fi', release_date=date(2010, 7, 16)
    )
    session.add(filme)
    session.commit()
    session.refresh(filme)

    return filme


@pytest.fixture
def movie_nao_visto(session):
    filme = Movie(
        title='The Matrix', genres='Sci-Fi', release_date=date(1999, 3, 31)
    )
    session.add(filme)
    session.commit()
    session.refresh(filme)

    return filme
