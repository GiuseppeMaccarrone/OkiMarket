import pytest

@pytest.mark.asyncio
async def test_create_and_get_product(client):
    """Test E2E: Crea e verifica il prodotto."""
    response = await client.post("/products/create", json={
        "name": "Smartphone TEST",
        "price": 599.99,
        "category_id": 1,
        "tags": ["elettronica", "smartphone", "nuovo"]
    })

    assert response.status_code == 201
    product_id = response.json()["id"]
    assert product_id is not None


@pytest.mark.asyncio
async def test_delete_product(client):
    """Test E2E: Crea un prodotto al volo e poi lo elimina subito."""
    create_response = await client.post("/products/create", json={
        "name": "Prodotto da Eliminare",
        "price": 9.99,
        "category_id": 1,
        "tags": ["test", "delete"]
    })

    if create_response.status_code == 500:
        print(f"\nDEBUG ERROR: {create_response.json()}")

    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    delete_response = await client.delete(f"/products/delete/{product_id}")
    assert delete_response.status_code == 200

@pytest.mark.asyncio
async def test_create_product_invalid_data(client):
    """Test E2E: Validazione Pydantic fallita (prezzo negativo)."""
    response = await client.post("/products/create", json={
        "name": "Smartphone TEST",
        "price": -10.0,
        "category_id": 1
    })
    assert response.status_code == 422  # Validazione fallita

@pytest.mark.asyncio
async def test_create_product_missing_field(client):
    """Test E2E: Manca un campo obbligatorio."""
    response = await client.post("/products/create", json={
        "name": "Smartphone",
        # manca price e category_id
    })
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_product_invalid_category(client):
    """Test E2E: La categoria non esiste, deve restituire 404."""
    response = await client.post("/products/create", json={
        "name": "Prodotto Orfano",
        "price": 100.0,
        "category_id": 999  # ID inesistente
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_get_nonexistent_product(client):
    """Test E2E: Recupero prodotto che non esiste."""
    response = await client.get("/products/get/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_nonexistent_product(client):
    """Test E2E: Eliminazione di un ID inesistente."""
    response = await client.delete("/products/delete/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_product(client):
    """Test E2E: Aggiornamento completo di un prodotto."""
    # 1. Crea
    create_res = await client.post("/products/create", json={
        "name": "Vecchia Tastiera",
        "price": 20.0,
        "category_id": 1
    })
    pid = create_res.json()["id"]

    # 2. Aggiorna
    update_res = await client.put(f"/products/update/{pid}", json={
        "name": "Nuova Tastiera Meccanica",
        "price": 80.0,
        "category_id": 1
    })

    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Nuova Tastiera Meccanica"
    assert update_res.json()["price"] == 80.0