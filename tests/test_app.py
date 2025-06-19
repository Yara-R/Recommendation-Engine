from fastapi.testclient import TestClient

from recommender.app import app

"""
A estrutura de um teste, costuma contar com 3 ou 4 fases importantes.

- A: Arrange (Organizar)
- A: Act (Executa a coisa - o SUT- System Under Test)
- A: Assert (garante que o resultado é o esperado)
"""


def test_read_root():
    # arrange
    client = TestClient(app)

    # act
    response = client.get('/')

    # assert
    assert response.json() == {'message': 'Welcome to the Recommender API'}
