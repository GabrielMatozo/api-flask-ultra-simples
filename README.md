# API Flask Ultra Simples

API RESTful em **Flask** com CRUD de carros, **MySQL + SQLAlchemy**, validação Marshmallow, **Swagger**, paginação, filtros e cobertura de testes — em Docker.

## Badges

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3-000000?style=flat&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-5.7-4479A1?style=flat&logo=mysql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-E34F26?style=flat)
![Swagger](https://img.shields.io/badge/Swagger-UI-85EA2D?style=flat&logo=swagger&logoColor=black)
![Docker](https://img.shields.io/badge/docker-ready-2496ED?style=flat&logo=docker&logoColor=white)
![Testes](https://img.shields.io/badge/testes-16%20passando-2EA44F?style=flat)
![Licença](https://img.shields.io/badge/licença-MIT-265CA0?style=flat)

## Problema → Solução

**Problema:** prototipar rapidamente uma API RESTful em Flask com banco relacional, validação, documentação interativa e testes, sem complexidade excessiva.

**Solução:** API enxuta com **app factory**, CRUD completo de carros (`/carros`), **paginação** e **filtros** (marca, modelo, ano), validação com **Marshmallow**, **Swagger UI** automática em `/apidocs/`, **health check**, **CORS** e **rate limiting** — tudo orquestrado via **Docker Compose** (API + MySQL 5.7 com healthcheck).

## Arquitetura

```
Cliente ──► Flask (CORS + Limiter 100/h)
              │
              ├── GET/POST /carros          → listar (paginado/filtrável) e criar
              ├── PUT/DELETE /carros/:id    → atualizar e remover
              ├── GET /health               → health check
              └── GET /apidocs/             → Swagger UI (flasgger)
                      │
                      ▼
              SQLAlchemy ──► MySQL (CarrosDB)
```

App factory (`create_app`) registra o blueprint `carros`, handlers de erro globais, inicializa o Swagger e aguarda o banco ficar pronto (`_wait_for_db`, com retry de 15s) antes de criar as tabelas.

## Stack

| Camada         | Tecnologia                                |
|----------------|-------------------------------------------|
| Linguagem      | Python 3.12                               |
| Framework      | Flask + flasgger (Swagger UI)             |
| Banco de dados | MySQL 5.7 + SQLAlchemy 2                  |
| Validação      | Marshmallow + marshmallow-sqlalchemy      |
| Extras         | Flask-CORS, Flask-Limiter, python-dotenv  |
| Testes         | pytest (SQLite em memória)                |
| Infra          | Docker Compose (api + db)                 |

## Quickstart

### Docker (recomendado)

```bash
docker compose up --build
```

- API: `http://localhost:5000`
- Swagger UI: `http://localhost:5000/apidocs/`

O contêiner `db` inicializa o banco com o script `db/CreateDataBase.sql` e o `api` só sobe após o MySQL ficar saudável.

### Desenvolvimento local

```bash
cp .env.example .env      # ajuste DATABASE_URL se necessário
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py             # ou: flask run --host=0.0.0.0
```

> Exigência: MySQL acessível (default `mysql+mysqlconnector://RootUser:MainPassword@localhost:3306/CarrosDB`).

### Endpoints

| Método | Rota            | Descrição                     |
|--------|-----------------|-------------------------------|
| GET    | `/carros`       | Listar (paginado + filtros)   |
| POST   | `/carros`       | Criar carro                   |
| PUT    | `/carros/{id}`  | Atualizar carro               |
| DELETE | `/carros/{id}`  | Remover carro                 |
| GET    | `/health`       | Health check                  |
| GET    | `/apidocs/`     | Swagger UI                    |

Exemplo:

```bash
curl -X POST http://localhost:5000/carros \
  -H "Content-Type: application/json" \
  -d '{"marca": "Fiat", "modelo": "Uno", "ano": 2020}'

curl "http://localhost:5000/carros?marca=Fiat&page=1&per_page=10"
```

## Screenshot

![Swagger UI da API](docs/SCREENSHOT.png)

## Testes

```bash
pytest -v    # 16 testes
```

Os testes usam **SQLite em memória** (override de config) — não precisam de MySQL rodando.

## Roadmap / Status

**Status:** funcional. **Roadmap:**

- [ ] Autenticação nos endpoints (JWT/API key)
- [ ] Migrações versionadas (Alembic)
- [ ] Deploy com Gunicorn e proxy (Nginx)

## Licença

[MIT](LICENSE)