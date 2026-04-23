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