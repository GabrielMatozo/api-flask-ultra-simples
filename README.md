

# API Flask Ultra Simples

Este projeto foi desenvolvido para relembrar conceitos básicos do Flask. Ele implementa uma API RESTful simples utilizando Flask e MySQL para cadastro e consulta de carros.

## Funcionalidades
- Listar todos os carros cadastrados (`GET /carros`)
- Cadastrar um novo carro (`POST /carros`)
- Atualizar um carro existente (`PUT /carros/<id>`)
- Remover um carro existente (`DELETE /carros/<id>`)

## Estrutura do Projeto
```
app.py                 # Código principal da API Flask
Dockerfile             # (Opcional) Dockerização do projeto
docker-compose.yml     # (Opcional) Orquestração dos containers (API + MySQL)
db/CreateDataBase.sql  # Script SQL para criar o banco de dados e tabela
```

## Instalação
1. Clone este repositório:
   ```sh
   git clone https://github.com/GabrielMatozo/api-flask-ultra-simples
   cd api-flask-ultra-simples
   ```
2. Instale as dependências do Python:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure o banco de dados MySQL usando o script em `db/CreateDataBase.sql`.
4. Ajuste as credenciais de acesso ao banco em `app.py` se necessário.

## Utilizando Docker Compose
Se preferir, você pode subir o ambiente completo (API + banco de dados) usando Docker Compose. Certifique-se de ter o Docker e o Docker Compose instalados.

Para subir os containers:
```sh
docker-compose up
```
Isso irá criar e iniciar os serviços definidos no arquivo `docker-compose.yml`.

Para parar os containers:
```sh
docker-compose down
```

## Como executar
```sh
python app.py
```
A API estará disponível em: http://localhost:5000

## Exemplos de uso

### Listar carros
```sh
curl http://localhost:5000/carros
```

### Cadastrar carro
```sh
curl -X POST http://localhost:5000/carros -H "Content-Type: application/json" -d '{"marca": "Fiat", "modelo": "Uno", "ano": 2010}'
```

### Atualizar carro
```sh
curl -X PUT http://localhost:5000/carros/1 -H "Content-Type: application/json" -d '{"marca": "Fiat", "modelo": "Palio", "ano": 2012}'
```

### Remover carro
```sh
curl -X DELETE http://localhost:5000/carros/1
```

---

Feito por Gabriel Matozo
