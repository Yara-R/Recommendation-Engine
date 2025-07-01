from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from recommender.database import get_session
from recommender.models import (
    Movie,
    Sessions,
    User,
    UserMovieInteraction,
)
from recommender.schemas import (
    EncerrarSessaoSchema,
    Message,
    MessageSchema,
    MovieSchema,
    RespostaRegistrada,
    RespostaSchema,
    SessaoResponse,
    SessaoSchema,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI()
origins = ['http://localhost:4200']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'Welcome to the Recommender API'}


@app.post(
    '/usuario/', status_code=HTTPStatus.CREATED, response_model=UserPublic
)
def criar_usuario(user: UserSchema, session: Session = Depends(get_session)):
    db_user = User(age=user.age, gender=user.gender)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/usuario/', response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.post(
    '/sessao', response_model=SessaoResponse, status_code=HTTPStatus.CREATED
)
def iniciar_sessao(
    sessao: SessaoSchema, session: Session = Depends(get_session)
):
    user = session.get(User, sessao.user_id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Usuário não encontrado'
        )

    nova_sessao = Sessions(user_id=sessao.user_id)
    session.add(nova_sessao)
    session.commit()
    session.refresh(nova_sessao)

    return {'session_id': nova_sessao.session_id}


@app.get('/filme', response_model=MovieSchema)
def recomendar_filme(user_id: int, session: Session = Depends(get_session)):
    # Filmes já vistos pelo usuário
    vistos = session.scalars(
        select(UserMovieInteraction.movie_id).where(
            UserMovieInteraction.user_id == user_id
        )
    ).all()

    filme = session.scalars(
        select(Movie).where(Movie.movie_id.notin_(vistos)).limit(1)
    ).first()

    if not filme:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Nenhum filme para recomendar',
        )

    return filme


@app.post(
    '/responder',
    response_model=RespostaRegistrada,
    status_code=HTTPStatus.CREATED,
)
def registrar_resposta(
    resposta: RespostaSchema, session: Session = Depends(get_session)
):
    # Verificações básicas (opcional mas recomendado)
    if not session.get(Sessions, resposta.session_id):
        raise HTTPException(status_code=404, detail='Sessão não encontrada')
    if not session.get(User, resposta.user_id):
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    if not session.get(Movie, resposta.movie_id):
        raise HTTPException(status_code=404, detail='Filme não encontrado')

    # Criar a interação
    interacao = UserMovieInteraction(
        session_id=resposta.session_id,
        user_id=resposta.user_id,
        movie_id=resposta.movie_id,
        response=resposta.response,
    )
    session.add(interacao)
    session.commit()
    session.refresh(interacao)

    return interacao


@app.post('/desistir', response_model=MessageSchema, status_code=HTTPStatus.OK)
def encerrar_sessao(
    dados: EncerrarSessaoSchema,
    session: Session = Depends(get_session),
):
    sessao = session.get(Sessions, dados.session_id)
    if not sessao:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Sessão não encontrada'
        )

    sessao.end_time = func.now()
    session.commit()

    return {'message': 'Sessão encerrada'}
