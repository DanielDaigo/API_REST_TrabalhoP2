from decimal import Decimal


def assert_item(item: dict, item_id: int, name: str, description: str | None, price: Decimal, quantity: int):
    assert item["id"] == item_id
    assert item["name"] == name
    assert item["description"] == description
    assert Decimal(item["price"]) == price
    assert item["quantity"] == quantity


def test_create_item_returns_201_and_created_data(client):
    payload = {
        "name": "Notebook",
        "description": "Notebook Dell",
        "price": 3500.00,
        "quantity": 10,
    }

    response = client.post("/items", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert_item(
        item=body,
        item_id=1,
        name="Notebook",
        description="Notebook Dell",
        price=Decimal("3500.00"),
        quantity=10,
    )


def test_read_items_returns_200_and_created_items(client):
    client.post(
        "/items",
        json={
            "name": "Mouse",
            "description": "Mouse sem fio",
            "price": 89.90,
            "quantity": 25,
        },
    )
    client.post(
        "/items",
        json={
            "name": "Teclado",
            "description": None,
            "price": 149.99,
            "quantity": 15,
        },
    )

    response = client.get("/items")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["name"] == "Mouse"
    assert body[0]["description"] == "Mouse sem fio"
    assert Decimal(body[0]["price"]) == Decimal("89.90")
    assert body[0]["quantity"] == 25
    assert body[1]["name"] == "Teclado"
    assert body[1]["description"] is None
    assert Decimal(body[1]["price"]) == Decimal("149.99")
    assert body[1]["quantity"] == 15


def test_read_item_returns_200_and_item_data(client):
    create_response = client.post(
        "/items",
        json={
            "name": "Monitor",
            "description": "Monitor 24 polegadas",
            "price": 1200.50,
            "quantity": 5,
        },
    )
    item_id = create_response.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert_item(
        item=response.json(),
        item_id=item_id,
        name="Monitor",
        description="Monitor 24 polegadas",
        price=Decimal("1200.50"),
        quantity=5,
    )


def test_read_item_returns_404_when_not_found(client):
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_item_returns_200_and_updated_data(client):
    create_response = client.post(
        "/items",
        json={
            "name": "Cadeira",
            "description": "Cadeira ergonômica",
            "price": 650.00,
            "quantity": 8,
        },
    )
    item_id = create_response.json()["id"]

    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "Cadeira Gamer",
            "description": "Cadeira ergonômica premium",
            "price": 780.90,
            "quantity": 12,
        },
    )

    assert response.status_code == 200
    assert_item(
        item=response.json(),
        item_id=item_id,
        name="Cadeira Gamer",
        description="Cadeira ergonômica premium",
        price=Decimal("780.90"),
        quantity=12,
    )


def test_update_item_returns_404_when_not_found(client):
    response = client.put(
        "/items/999",
        json={
            "name": "Item inexistente",
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_delete_item_returns_200_and_removes_item(client):
    create_response = client.post(
        "/items",
        json={
            "name": "Impressora",
            "description": "Impressora laser",
            "price": 900.00,
            "quantity": 3,
        },
    )
    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/items/{item_id}")
    read_response = client.get(f"/items/{item_id}")

    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Item deleted"
    assert read_response.status_code == 404
    assert read_response.json()["detail"] == "Item not found"


def test_delete_item_returns_404_when_not_found(client):
    response = client.delete("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
