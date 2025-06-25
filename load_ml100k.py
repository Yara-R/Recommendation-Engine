import os
from datetime import datetime

from recommender.models import (
    Movie,
    MovieResponse,
    Sessions,
    User,
    UserMovieInteraction,
    table_registry,
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Constantes para conversão de ratings
MAX_RATING_NAO = 2
RATING_MAYBE = 3
BATCH_SIZE = 1000
PROGRESS_INTERVAL = 10000

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%d-%b-%Y").date()
    except Exception:
        return None

def load_movies_data():
    """
    Carrega os dados dos filmes do arquivo u.item
    """
    # O arquivo u.item contém informações dos filmes

    movies_data = []

    with open('ml-100k/u.item', 'r', encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split('|')
            movie_id = int(parts[0])
            title = parts[1]
            release_date = parse_date(parts[2])  # formato: dd-MMM-yyyy

            

            # Extrair gêneros (últimas 19 colunas são gêneros binários)
            genre_columns = parts[5:]  # Pula os primeiros 5 campos
            genre_names = [
                'unknown',
                'Action',
                'Adventure',
                'Animation',
                'Children',
                'Comedy',
                'Crime',
                'Documentary',
                'Drama',
                'Fantasy',
                'Film-Noir',
                'Horror',
                'Musical',
                'Mystery',
                'Romance',
                'Sci-Fi',
                'Thriller',
                'War',
                'Western',
            ]

            # Identificar gêneros ativos
            active_genres = []
            for i, genre_val in enumerate(genre_columns):
                if genre_val == '1' and i < len(genre_names):
                    active_genres.append(genre_names[i])

            genres = '|'.join(active_genres) if active_genres else 'unknown'

            movies_data.append({
                'movie_id': movie_id,
                'title': title,
                'release_date': release_date,
                'genres': genres,
            })

    return movies_data


def load_users_data():
    """
    Carrega os dados dos usuários do arquivo u.user
    """
    # O arquivo u.user contém: user_id | age | gender | occupation | zip_code

    users_data = []

    with open('ml-100k/u.user', 'r', encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split('|')
            user_id = int(parts[0])
            age = int(parts[1])
            gender = parts[2]

            # Criar username e email fictícios baseados no user_id
            username = f'user_{user_id}'
    

            users_data.append({
                'user_id': user_id,
                'username': username,
                'age': age,
                'gender': gender
            })

    return users_data


def load_ratings_data():
    """
    Carrega os dados de avaliações do arquivo u.data
    """
    # O arquivo u.data contém: user_id | movie_id | rating | timestamp

    ratings_data = []

    with open('ml-100k/u.data', 'r', encoding='latin-1') as f:
        for line in f:
            parts = line.strip().split('\t')
            user_id = int(parts[0])
            movie_id = int(parts[1])
            rating = int(parts[2])
            timestamp = int(parts[3])

            # Converter rating para MovieResponse
            # Rating 1-2: nao, Rating 3: nao_mas_quero, Rating 4-5: sim
            if rating <= MAX_RATING_NAO:
                response = "nao"
            elif rating == RATING_MAYBE:
                response = "nao_mas_quero"
            else:
                response = "sim"

            ratings_data.append({
                'user_id': user_id,
                'movie_id': movie_id,
                'response': response,
                'timestamp': timestamp,
            })

    return ratings_data


def create_database_session(database_url='sqlite:///movielens.db'):
    """
    Cria a sessão do banco de dados
    """
    engine = create_engine(database_url)

    # Criar todas as tabelas
    table_registry.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session()


def insert_movies(db_session, movies_data):
    """Insere filmes no banco de dados"""
    print('Inserindo filmes...')
    for movie_data in movies_data:
        movie = Movie(
            title=movie_data['title'],
            release_date=movie_data['release_date'],
            genres=movie_data['genres'],
            
        )
        db_session.add(movie)

    db_session.commit()
    print('Filmes inseridos com sucesso!')


def insert_users(db_session, users_data):
    """Insere usuários no banco de dados"""
    print('Inserindo usuários...')
    for user_data in users_data:
        try:
            user = User(
                username=user_data['username'],
                age=user_data['age'],
                gender=user_data['gender'],
            )
            db_session.add(user)
        except Exception as e:
            print(f'Erro ao inserir usuário {user_data["username"]}: {e}')
            print(f'Dados do usuário: {user_data}')
            raise

    db_session.commit()
    print('Usuários inseridos com sucesso!')


def create_user_sessions(db_session):
    """Cria sessões para cada usuário"""
    print('Criando sessões...')
    users = db_session.query(User).all()
    user_sessions = {}

    for user in users:
        session = Sessions(user_id=user.user_id, responses_count=0)
        db_session.add(session)
        db_session.flush()  # Para obter o session_id
        user_sessions[user.user_id] = session.session_id

    db_session.commit()
    print('Sessões criadas com sucesso!')
    return user_sessions


def insert_interactions(db_session, ratings_data, user_sessions):
    """Insere interações no banco de dados"""
    print('Inserindo interações...')
    for i, rating_data in enumerate(ratings_data):
        if i % PROGRESS_INTERVAL == 0:
            print(f'Processando interação {i + 1}/{len(ratings_data)}')

        interaction = UserMovieInteraction(
            session_id=user_sessions[rating_data['user_id']],
            user_id=rating_data['user_id'],
            movie_id=rating_data['movie_id'],
            response=rating_data['response'],
        )
        db_session.add(interaction)

        # Commit em lotes para melhor performance
        if i % BATCH_SIZE == 0:
            db_session.commit()

    db_session.commit()
    print('Interações inseridas com sucesso!')


def update_session_counters(db_session, user_sessions):
    """Atualiza contadores de respostas nas sessões"""
    print('Atualizando contadores de sessões...')
    for user_id, session_id in user_sessions.items():
        count = (
            db_session.query(UserMovieInteraction)
            .filter_by(session_id=session_id)
            .count()
        )
        session = (
            db_session.query(Sessions).filter_by(session_id=session_id).first()
        )
        session.responses_count = count

    db_session.commit()
    print('Contadores atualizados!')


def populate_database():
    """
    Popula o banco de dados com os dados do MovieLens
    """
 

    print('Carregando dados dos arquivos...')

    # Carregar dados
    movies_data = load_movies_data()
    users_data = load_users_data()
    ratings_data = load_ratings_data()

    print(f'Carregados {len(movies_data)} filmes')
    print(f'Carregados {len(users_data)} usuários')
    print(f'Carregadas {len(ratings_data)} avaliações')

    # Debug: verificar dados do primeiro usuário
    if users_data:
        print(f'Debug - Primeiro usuário: {users_data[0]}')

    # Criar sessão do banco
    db_session = create_database_session()

    try:
        # Executar inserções
        insert_movies(db_session, movies_data)
        insert_users(db_session, users_data)
        user_sessions = create_user_sessions(db_session)
        insert_interactions(db_session, ratings_data, user_sessions)
        update_session_counters(db_session, user_sessions)

        print('\n✅ Banco de dados populado com sucesso!')
        print(f'Total de filmes: {len(movies_data)}')
        print(f'Total de usuários: {len(users_data)}')
        print(f'Total de interações: {len(ratings_data)}')

    except Exception as e:
        print(f'Erro ao popular banco de dados: {e}')
        db_session.rollback()
        raise  # Re-raise para ver o traceback completo
    finally:
        db_session.close()


def verify_data():
    """
    Verifica se os dados foram inseridos corretamente
    """
    db_session = create_database_session()

    try:
        movies_count = db_session.query(Movie).count()
        users_count = db_session.query(User).count()
        sessions_count = db_session.query(Sessions).count()
        interactions_count = db_session.query(UserMovieInteraction).count()

        print('\n📊 Verificação do banco de dados:')
        print(f'Filmes: {movies_count}')
        print(f'Usuários: {users_count}')
        print(f'Sessões: {sessions_count}')
        print(f'Interações: {interactions_count}')

        # Mostrar alguns exemplos
        print('\n🎬 Exemplo de filmes:')
        movies = db_session.query(Movie).limit(3).all()
        for movie in movies:
            release_info = (
                f' ({movie.release_date.year})' if movie.release_date else ''
            )

            print(f'- {movie.title}{release_info} - {movie.genres}')

        print('\n👤 Exemplo de usuários:')
        users = db_session.query(User).limit(3).all()
        for user in users:
            print(f'- {user.username}')

        print('\n⭐ Exemplo de interações:')
        interactions = db_session.query(UserMovieInteraction).limit(3).all()
        for interaction in interactions:
            movie = (
                db_session.query(Movie)
                .filter_by(movie_id=interaction.movie_id)
                .first()
            )
            user = (
                db_session.query(User)
                .filter_by(user_id=interaction.user_id)
                .first()
            )
            print(
                f'- {user.username} → {movie.title}: '
                f'{interaction.response.value}'
            )

    finally:
        db_session.close()


if __name__ == '__main__':
    print('🎬 Carregador do Dataset MovieLens 100K')
    print('=' * 40)

    # Executar o processo
    populate_database()
    verify_data()

    print('\n✅ Processo concluído!')
