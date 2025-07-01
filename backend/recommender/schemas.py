from datetime import date
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    age: int
    gender: str


class UserPublic(BaseModel):
    uuid: UUID
    age: int
    gender: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


# Schema de entrada
class SessaoSchema(BaseModel):
    user_id: int


# Schema de resposta
class SessaoResponse(BaseModel):
    session_id: int


class MovieResponse(str, Enum):
    sim = 'sim'
    nao = 'nao'
    nao_mas_quero = 'nao_mas_quero'


class RespostaSchema(BaseModel):
    session_id: int
    user_id: int
    movie_id: int
    response: MovieResponse


# Schema de resposta
class RespostaRegistrada(BaseModel):
    interaction_id: int
    session_id: int
    user_id: int
    movie_id: int
    response: MovieResponse


class MovieSchema(BaseModel):
    movie_id: int
    title: str
    genres: str
    release_date: Optional[date]


class EncerrarSessaoSchema(BaseModel):
    session_id: int


class MessageSchema(BaseModel):
    message: str
