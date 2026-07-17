# API Flask Ultra Simples

API RESTful em Flask para cadastro e consulta de carros, com MySQL, SQLAlchemy, validação, testes, Docker, Swagger, paginação e filtros.

## Funcionalidades

- CRUD completo de carros (`GET/POST/PUT/DELETE /carros`)
- Paginação (`?page=1&per_page=10`)
- Filtros por marca, modelo e ano (`?marca=Fiat&ano=2020`)
- Validação de payload (Marshmallow)
- Swagger UI em `/apidocs/`
- Health check (`GET /health`)
- CORS habilitado
- Rate limiting (100 req/hora)
- Docker Compose (Flask + MySQL)
- Testes com pytest (16 testes)

## Estrutura

```
├── app/
│   ├── __init__.py          # App factory, CORS, Swagger, rate limit
│   ├── config.py            # Config via .env (DATABASE_URL)
│   ├── models.py            # SQLAlchemy (Carro)
│   ├── schemas.py           # Marshmallow schemas
│   ├── errors.py            # Error handlers globais
│   └── routes/
│       └── carros.py        # Blueprint CRUD + paginação + filtros
├── tests/
│   ├── conftest.py          # Fixtures (SQLite in-memory)
│   └── test_carros.py       # 16 testes
├── db/
│   └── CreateDataBase.sql   # Script de inicialização do MySQL
├── .env.example             # Template de variáveis de ambiente
├── Dockerfile               # Imagem Python 3.12-slim
├── docker-compose.yml       # API + MySQL com healthcheck
└── requirements.txt
```

## Docker (recomendado)

```sh
docker compose up --build
```

A API estará em `http://localhost:5000` e o Swagger em `http://localhost:5000/apidocs/`.

## Desenvolvimento local

```sh
cp .env.example .env
pip install -r requirements.txt
python app.py
```

## Testes

```sh
pytest -v
```

Usa SQLite em memória — não precisa de MySQL rodando.

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/carros` | Listar carros (paginado, filtrável) |
| POST | `/carros` | Criar carro |
| PUT | `/carros/{id}` | Atualizar carro |
| DELETE | `/carros/{id}` | Remover carro |
| GET | `/health` | Health check |
| GET | `/apidocs/` | Swagger UI |

---

Feito por Gabriel Matozo
