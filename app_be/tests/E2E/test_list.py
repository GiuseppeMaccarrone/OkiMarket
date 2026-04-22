
import pytest

@pytest.mark.asyncio
async def test_filter_by_search(client):
    response = await client.get("/products/list", params={"search": "Monitor"})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Monitor 4K"

@pytest.mark.asyncio
async def test_filter_by_category(client):
    # La categoria 1 ha Mouse e Tastiera
    response = await client.get("/products/list", params={"category_id": 1})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["category_id"] == 1
    assert data[1]["category_id"] == 1

@pytest.mark.asyncio
async def test_filter_by_min_price(client):
    # Solo Monitor costa più di 100
    response = await client.get("/products/list", params={"min_price": 100.00})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Monitor 4K"

@pytest.mark.asyncio
async def test_filter_by_max_price(client):
    # Solo Mouse costa meno di 20
    response = await client.get("/products/list", params={"max_price": 20.00})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mouse Economico"

@pytest.mark.asyncio
async def test_filter_range_and_search_combined(client):
    # Cerca qualcosa che costa tra 50 e 100
    response = await client.get("/products/list", params={
        "min_price": 50.00,
        "max_price": 100.00
    })
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Tastiera Meccanica"

@pytest.mark.asyncio
async def test_sorting_price_asc(client):
    # Ordine crescente di prezzo
    response = await client.get("/products/list", params={"sort_by": "price_asc"})
    assert response.status_code == 200

    data = response.json()
    assert data[0]["name"] == "Mouse Economico"  # 10
    assert data[1]["name"] == "Tastiera Meccanica"  # 80
    assert data[2]["name"] == "Monitor 4K"  # 300

@pytest.mark.asyncio
async def test_filter_empty_result(client):
    # Prezzo impossibile
    response = await client.get("/products/list", params={"min_price": 9999.00})
    assert response.status_code == 200

    data = response.json()
    assert data == []  # Deve essere una lista vuota, non un errore 404 o 500