# Passo a passo para testar a aplicação

## 1. Verifique se a venv está ativada

No PowerShell, rode:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativada, deve aparecer algo como:

```powershell
(.venv)
```

Caso dê erro de permissão, rode uma vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Depois tente ativar novamente:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 2. Instale as dependências

Com a venv ativada:

```powershell
pip install -r requirements.txt
```

---

## 3. Suba o banco PostgreSQL com Docker

Em um terminal, rode:

```powershell
docker compose up db
```

Deixe esse terminal aberto.

---

## 4. Abra um segundo terminal e inicie a API

Antes de iniciar a API localmente, configure o banco para usar `localhost`:

```powershell
$env:DB_HOST="localhost"
```

Ative a venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

Inicie a API:

```powershell
uvicorn app.main:app --reload
```

---

## 5. Abra um terceiro terminal para os testes

Ative a venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 6. Rode os testes automatizados

```powershell
pytest
```

Se tudo estiver correto, você deve ver algo como:

```text
8 passed
```

ou:

```text
tests/test_items_api.py ........                                         [100%]
```

---

## 7. Teste o endpoint de saúde

Abra no navegador:

```text
http://localhost:8000/health
```

Ou use:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

---

## 8. Teste o CRUD manualmente

### Criar item

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/items" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"name":"Notebook","description":"Notebook Dell","price":3500.00,"quantity":10}'
```

Resposta esperada:

```json
{
  "id": 1,
  "name": "Notebook",
  "description": "Notebook Dell",
  "price": "3500.00",
  "quantity": 10
}
```

Anote o `id` retornado. Nos exemplos abaixo, será usado o `id` `1`.

---

### Listar itens

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/items" -Method Get
```

Resposta esperada:

```json
[
  {
    "id": 1,
    "name": "Notebook",
    "description": "Notebook Dell",
    "price": "3500.00",
    "quantity": 10
  }
]
```

---

### Buscar item por ID

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/items/1" -Method Get
```

Resposta esperada:

```json
{
  "id": 1,
  "name": "Notebook",
  "description": "Notebook Dell",
  "price": "3500.00",
  "quantity": 10
}
```

---

### Atualizar item

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/items/1" `
  -Method Put `
  -ContentType "application/json" `
  -Body '{"name":"Notebook Pro","description":"Notebook Dell atualizado","price":3900.00,"quantity":7}'
```

Resposta esperada:

```json
{
  "id": 1,
  "name": "Notebook Pro",
  "description": "Notebook Dell atualizado",
  "price": "3900.00",
  "quantity": 7
}
```

---

### Deletar item

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/items/1" -Method Delete
```

Resposta esperada:

```json
{
  "detail": "Item deleted"
}
```

---

### Confirmar exclusão

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/items/1" -Method Get
```

Resposta esperada:

```json
{
  "detail": "Item not found"
}
```

---

## 10. Teste rodando tudo com Docker Compose

Primeiro, pare o `uvicorn` local se estiver rodando.

Depois rode:

```powershell
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

Documentação automática:

```text
http://localhost:8000/docs
```

Saúde:

```text
http://localhost:8000/health
```

---

## 11. Teste dentro do container Docker

Com a aplicação rodando via Docker, abra outro terminal e rode:

```powershell
docker compose exec api pytest
```

Se tudo estiver correto, os testes devem passar.

---

## 12. Parar os containers

Para parar tudo:

```powershell
docker compose down
```

Se quiser parar e remover também o volume do banco:

```powershell
docker compose down -v
```

Atenção: `docker compose down -v` apaga os dados do banco PostgreSQL.

</contents>
