from http import HTTPStatus


def test_root(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Welcome to the Recommender API'}


# Testes para o endpoint de criação e leitura de usuários
def test_create_user(client):
    response = client.post(
        '/usuario/',
        json={
            'username': 'alice',
            'age': 30,
            'gender': 'F',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'user_id': 1,
        'username': 'alice',
        'age': 30,
        'gender': 'F',
    }


def test_create_user_with_existing_username(client):
    client.post(
        '/usuario/',
        json={'username': 'duplicado', 'age': 30, 'gender': 'F'},
    )

    response = client.post(
        '/usuario/',
        json={'username': 'duplicado', 'age': 30, 'gender': 'F'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_delete_user_should_return_not_found(client):
    response = client.delete('/usuario/10000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/usuario/10000',
        json={'username': 'bob', 'age': 25, 'gender': 'M'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_get_user_should_return_not_found(client):
    response = client.get('/usuario/10000')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_read_users(client):
    response = client.get('/usuario/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


# Testes para o endpoint de iniciar sessão
def test_iniciar_sessao(client):
    response = client.post(
        '/usuario/',
        json={
            'username': 'alice',
            'age': 30,
            'gender': 'F',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post('/sessao', json={'user_id': 1})

    assert response.status_code == HTTPStatus.CREATED
    assert 'session_id' in response.json()


# Testes para o endpoint de registrar resposta
def test_registrar_resposta_sim(client, user, movie):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post(
        '/responder',
        json={
            'session_id': session_id,
            'user_id': user.user_id,
            'movie_id': movie.movie_id,
            'response': 'sim',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'interaction_id' in response.json()


def test_registrar_resposta_nao(client, user, movie):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post(
        '/responder',
        json={
            'session_id': session_id,
            'user_id': user.user_id,
            'movie_id': movie.movie_id,
            'response': 'nao',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'interaction_id' in response.json()


def test_registrar_resposta_nao_mas_quero(client, user, movie):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post(
        '/responder',
        json={
            'session_id': session_id,
            'user_id': user.user_id,
            'movie_id': movie.movie_id,
            'response': 'nao_mas_quero',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert 'interaction_id' in response.json()


def test_registrar_resposta_sessao_inexistente(client, user, movie):
    response = client.post(
        '/responder',
        json={
            'session_id': 9999,
            'user_id': user.user_id,
            'movie_id': movie.movie_id,
            'response': 'sim',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Sessão não encontrada'}


def test_registrar_resposta_usuario_inexistente_no_responder(client, movie):
    response = client.post(
        '/usuario/', json={'username': 'bob', 'age': 25, 'gender': 'M'}
    )
    assert response.status_code == HTTPStatus.CREATED
    user_id = response.json()['user_id']

    response = client.post('/sessao', json={'user_id': user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post(
        '/responder',
        json={
            'session_id': session_id,
            'user_id': 9999,  # usuário inexistente
            'movie_id': movie.movie_id,
            'response': 'sim',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}


def test_registrar_resposta_filme_inexistente(client, user):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post(
        '/responder',
        json={
            'session_id': session_id,
            'user_id': user.user_id,
            'movie_id': 9999,
            'response': 'sim',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Filme não encontrado'}


def test_recomendar_filme(client, user, movie, movie_nao_visto):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post(
        '/responder',
        json={
            'session_id': session_id,
            'user_id': user.user_id,
            'movie_id': movie.movie_id,
            'response': 'sim',
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.get(f'/filme?user_id={user.user_id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'movie_id': movie_nao_visto.movie_id,
        'title': movie_nao_visto.title,
        'genres': movie_nao_visto.genres,
        'release_date': movie_nao_visto.release_date.isoformat(),
    }


def test_recomendar_filme_sem_vistos(client, user):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED

    response = client.get(f'/filme?user_id={user.user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nenhum filme para recomendar'}


def test_recomendar_filme_usuario_inexistente(client):
    response = client.get('/filme?user_id=9999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nenhum filme para recomendar'}


def recomendar_filme_sem_ter_filmes_nao_vistos(client, user):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED

    # Simula que o usuário já viu todos os filmes
    response = client.get(f'/filme?user_id={user.user_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Nenhum filme para recomendar'}


def test_encerrar_sessao(client, user):
    response = client.post('/sessao', json={'user_id': user.user_id})
    assert response.status_code == HTTPStatus.CREATED
    session_id = response.json()['session_id']

    response = client.post('/desistir', json={'session_id': session_id})
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Sessão encerrada'}

    # Verifica se a sessão foi realmente encerrada
    response = client.get(f'/sessao/{session_id}')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Not Found'}


def test_encerrar_sessao_inexistente(client):
    response = client.post('/desistir', json={'session_id': 9999})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Sessão não encontrada'}


def test_encerrar_sessao_usuario_inexistente(client):
    response = client.post('/sessao', json={'user_id': 9999})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Usuário não encontrado'}

    response = client.post('/desistir', json={'session_id': 1})
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Sessão não encontrada'}


def test_encerrar_sessao_sem_usuario(client):
    response = client.post('/sessao')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        'detail': [
            {
                'input': None,
                'loc': ['body'],
                'msg': 'Field required',
                'type': 'missing',
            }
        ]
    }


def test_encerrar_sessao_sem_session_id(client):
    response = client.post('/desistir')
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        'detail': [
            {
                'input': None,
                'loc': ['body'],
                'msg': 'Field required',
                'type': 'missing',
            }
        ]
    }


def test_encerrar_sessao_sem_session_id_invalido(client):
    response = client.post('/desistir', json={'session_id': 'invalid'})
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json() == {
        'detail': [
            {
                'input': 'invalid',
                'loc': ['body', 'session_id'],
                'msg': 'Input should be a valid integer, '
                'unable to parse string as an integer',
                'type': 'int_parsing',
            }
        ]
    }
