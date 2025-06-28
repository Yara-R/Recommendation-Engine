from datetime import datetime

from sqlalchemy import select

from recommender.models import (
    Movie,
    MovieResponse,
    Sessions,
    User,
    UserMovieInteraction,
)

AGE = 23

def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='alice', gender='F', age=23)
        session.add(new_user)
        session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.user_id == 1
    assert user.username == 'alice'
    assert user.gender == 'F'
    assert user.age == AGE
    assert user.created_at == time


def test_create_movie(session):
    new_movie = Movie(
        title='The Matrix',
        genres='Action|Sci-Fi',
        release_date=datetime.strptime('21-May-1999', '%d-%b-%Y').date(),
    )
    session.add(new_movie)
    session.commit()

    movie = session.scalar(select(Movie).where(Movie.title == 'The Matrix'))

    assert movie is not None
    assert movie.title == 'The Matrix'
    assert movie.genres == 'Action|Sci-Fi'
    assert movie.release_date == datetime(1999, 5, 21).date()


def test_create_session(session, mock_db_time):
    new_user = User(username='alice', gender='F', age=23)
    session.add(new_user)
    session.commit()

    new_session = Sessions(user_id=new_user.user_id, responses_count=5)
    session.add(new_session)
    session.commit()

    created_session = session.scalar(
        select(Sessions).where(Sessions.user_id == new_user.user_id)
    )

    RESPONSES_COUNT = 5
    assert created_session.session_id == 1
    assert created_session.user_id == new_user.user_id
    assert created_session.start_time is not None
    assert created_session.end_time is not None
    assert created_session.responses_count == RESPONSES_COUNT


def test_interaction(session, mock_db_time):
    new_user = User(username='alice', gender='F', age=23)
    session.add(new_user)
    session.commit()

    new_movie = Movie(
        title='The Matrix',
        genres='Action|Sci-Fi',
        release_date=datetime.strptime('21-May-1999', '%d-%b-%Y').date(),
    )
    session.add(new_movie)
    session.commit()

    new_session = Sessions(user_id=new_user.user_id, responses_count=5)
    session.add(new_session)
    session.commit()

    new_interaction = UserMovieInteraction(
        user_id=new_user.user_id,
        movie_id=new_movie.movie_id,
        session_id=new_session.session_id,
        response=MovieResponse.sim,
    )
    session.add(new_interaction)
    session.commit()

    interaction = session.scalar(
        select(UserMovieInteraction).where(
            UserMovieInteraction.user_id == new_user.user_id
        )
    )

    assert interaction is not None
    assert interaction.user_id == new_user.user_id
    assert interaction.movie_id == new_movie.movie_id
    assert interaction.session_id == new_session.session_id
    assert interaction.response == MovieResponse.sim
