import enum
from datetime import datetime, date

from sqlalchemy import Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

# Registro de mapeamento
table_registry = registry()


# Enum para respostas
class MovieResponse(enum.Enum):
    sim = 'sim'
    nao = 'nao'
    nao_mas_quero = 'nao_mas_quero'


# Tabela de Usuários
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    age: Mapped[str]
    gender: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )

    sessions: Mapped[list['Sessions']] = relationship(
        back_populates='user', init=False
    )
    interactions: Mapped[list['UserMovieInteraction']] = relationship(
        back_populates='user', init=False
    )


# Tabela de Filmes
@table_registry.mapped_as_dataclass
class Movie:
    __tablename__ = 'movies'

    movie_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    genres: Mapped[str]
    release_date: Mapped[date | None] = mapped_column(nullable=True)


    interactions: Mapped[list['UserMovieInteraction']] = relationship(
        back_populates='movie', init=False
    )


# Tabela de Sessões
@table_registry.mapped_as_dataclass
class Sessions:
    __tablename__ = 'sessions'

    session_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))

    user: Mapped['User'] = relationship(back_populates='sessions', init=False)
    interactions: Mapped[list['UserMovieInteraction']] = relationship(
        back_populates='session', init=False
    )

    start_time: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    end_time: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    responses_count: Mapped[int] = mapped_column(default=0)


# Tabela de Interações
@table_registry.mapped_as_dataclass
class UserMovieInteraction:
    __tablename__ = 'user_movie_interactions'

    interaction_id: Mapped[int] = mapped_column(init=False, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('sessions.session_id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    movie_id: Mapped[int] = mapped_column(ForeignKey('movies.movie_id'))
    response: Mapped[MovieResponse] = mapped_column(
        Enum(MovieResponse, name='movie_response_enum')
    )

    session: Mapped['Sessions'] = relationship(
        back_populates='interactions', init=False
    )
    movie: Mapped['Movie'] = relationship(
        back_populates='interactions', init=False
    )
    user: Mapped['User'] = relationship(
        back_populates='interactions', init=False
    )
