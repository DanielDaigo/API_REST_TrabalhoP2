# Item Management API

API REST desenvolvida com **FastAPI** para gerenciamento de itens, com persistência em banco de dados relacional **PostgreSQL** executado via Docker.

## Tecnologias utilizadas

- Python 3.12
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Docker e Docker Compose
- Pytest

## Estrutura do projeto

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── crud.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_items_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── plan.md
```

## Execução com Docker

Com Docker e Docker Compose instalados, execute:

```powershell
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

A documentação automática do FastAPI estará disponível em:

```text
http://localhost:8000/docs
```

## Execução local com venv

Criar a venv:

```powershell
python -m venv .venv
```

Ativar a venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar dependências:

```powershell
pip install -r requirements.txt
```

Executar a API localmente:

```powershell
uvicorn app.main:app --reload
```

Para execução local também é necessário subir o banco:

```powershell
docker compose up db
```

## Variáveis de ambiente

A aplicação utiliza as seguintes variáveis de ambiente:

```text
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DB_NAME=itemsdb
```

Ao executar localmente fora do Docker, altere `DB_HOST` conforme necessário, por exemplo:

```powershell
$env:DB_HOST="localhost"
```

## Endpoints

### Saúde

```http
GET /health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

### Criar item

```http
POST /items
```

Exemplo de payload:

```json
{
  "name": "Notebook",
  "description": "Notebook Dell",
  "price": 3500.00,
  "quantity": 10
}
```

### Listar itens

```http
GET /items
```

Parâmetros opcionais:

```text
skip=0&limit=100
```

### Buscar item por ID

```http
GET /items/{item_id}
```

### Atualizar item

```http
PUT /items/{item_id}
```

Exemplo de payload:

```json
{
  "name": "Notebook Pro",
  "price": 3900.00
}
```

### Deletar item

```http
DELETE /items/{item_id}
```

## Execução dos testes

Com a venv ativada e o PostgreSQL executando via Docker:

```powershell
docker compose up db
pytest
```

Também é possível executar os testes dentro do container da API:

```powershell
docker compose exec api pytest
```

Os testes validam os códigos de resposta HTTP e os dados retornados para todas as operações CRUD:

- `POST /items`
- `GET /items`
- `GET /items/{item_id}`
- `PUT /items/{item_id}`
- `DELETE /items/{item_id}`

## Publicação no GitHub

Após validar a aplicação, publique o projeto em um repositório GitHub com:

```powershell
git init
git add .
git commit -m "Implementa API REST com FastAPI, Docker e testes"
git branch -M main
git remote add origin <URL_DO_REPOSITORIO>
git push -u origin main
```

</contents>