# Backend - Recommender

Este diretório contém o backend da aplicação **Recommender**, implementado em Python com FastAPI, SQLAlchemy e outras dependências. O backend oferece APIs para recomendação de filmes, manipulação de dados e integração com banco PostgreSQL.

---

## Pré-requisitos

- Python 3.13
- PostgreSQL
- Docker
- Poetry instalado

---

## Setup inicial

1. Clone o repositório e navegue até a pasta `backend`:

    ```bash
    git clone <url-do-repositorio>
    cd Recommendation-Engine/backend
    ```
2. Instale as dependências do Poetry:

    ```bash
    poetry install
    ```
3. Ative o ambiente virtual do Poetry:

    ```bash
    poetry shell
    ```

4. Instale as dependências, incluindo o grupo de desenvolvimento:

    ```bash
    poetry install --with dev
    ```

5. Configure variáveis de ambiente. Crie um arquivo `.env` na raiz do projeto com a seguinte variável:

    ```plaintext
    DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<banco>
    ```

6. Para rodar o backend com Docker Compose, execute:

    ```bash
    docker compose up --build
    ```

7. Se preferir rodar localmente sem Docker, certifique-se de que o PostgreSQL está rodando e execute:

    ```bash
    alembic upgrade head
    ```

## Rodando o backend

Para iniciar o servidor FastAPI localmente:

```bash
poetry shell

## Comandos úteis

O projeto usa taskipy para simplificar comandos. Para rodar uma tarefa:

```bash
task <nome-da-tarefa>
```

- task lint: executa a verificação de lint com o ruff

- task format: formata o código com o ruff

- task test: roda os testes com pytest, exibindo cobertura de código

- task run: inicia o servidor FastAPI local

## Estrutura do projeto

```plaintext
backend/
├── recommender/          # Código fonte do backend
├── migrations/           # Arquivos de migração do banco (Alembic)
├── tests/                # Testes unitários
├── Dockerfile            # Dockerfile para construir a imagem do backend
├── docker-compose.yml    # Configuração do Docker Compose
├── .env                  # Variáveis de ambiente (DATABASE_URL)
├── pyproject.toml        # Configurações do Poetry e definições do taskipy
└── README.md             # Este arquivo
```
