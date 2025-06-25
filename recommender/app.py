import random

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from recommender.database import get_db
from recommender.models import (
    Movie,
    MovieResponse,
    Sessions,
    UserMovieInteraction,
)
from recommender.schemas import Message

app = FastAPI()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Welcome to the Recommender API'}


# CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Lista de métodos de recomendação simulados
RECOMMENDATION_METHODS = [
    'clustering',
    'content_based',
    'regression',
    'collaborative',
]


def recommend_movie(user_id: int, db: Session, method: str) -> Movie:
    """Simula um sistema de recomendação usando métodos diversos"""
    seen_movie_ids = db.scalars(
        select(UserMovieInteraction.movie_id).where(
            UserMovieInteraction.user_id == user_id
        )
    ).all()

    query = select(Movie).where(Movie.movie_id.notin_(seen_movie_ids))
    result = db.scalars(query).all()
    if not result:
        raise HTTPException(
            status_code=404, detail='No more movies to recommend'
        )
    return random.choice(result)  # simula recomendação


@app.post('/start-session/{user_id}')
def start_session(user_id: int, db: Session = Depends(get_db)):
    session = Sessions(user_id=user_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return {'session_id': session.session_id}


@app.get('/next-movie/{user_id}/{session_id}')
def get_next_movie(
    user_id: int, session_id: int, db: Session = Depends(get_db)
):
    method = random.choice(RECOMMENDATION_METHODS)
    movie = recommend_movie(user_id, db, method)
    return {
        'movie_id': movie.movie_id,
        'title': movie.title,
        'genres': movie.genres,
        'method': method,
    }


@app.post('/respond')
def record_response(
    user_id: int,
    session_id: int,
    movie_id: int,
    response: MovieResponse,
    db: Session = Depends(get_db),
):
    interaction = UserMovieInteraction(
        user_id=user_id,
        session_id=session_id,
        movie_id=movie_id,
        response=response,
    )
    db.add(interaction)

    session = db.get(Sessions, session_id)
    session.responses_count += 1
    db.commit()
    return {'status': 'recorded', 'response': response.value}


@app.post('/end-session/{session_id}')
def end_session(session_id: int, db: Session = Depends(get_db)):
    session = db.get(Sessions, session_id)
    if not session:
        raise HTTPException(status_code=404, detail='Session not found')
    session.end_time = func.now()
    db.commit()
    return {'status': 'session ended'}
