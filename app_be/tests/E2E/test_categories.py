import pytest

@pytest.mark.asyncio
async def test_create_category(client):
    """Test E2E: Creazione di una nuova categoria."""
    response = await client.post("/categories/create", json={"name": "Sport"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Sport"
    assert "id" in data

@pytest.mark.asyncio
async def test_list_categories(client):
    """Test E2E: Lista categorie (dovrebbe trovarne 2 create dal setup_catalog)."""
    response = await client.get("/categories/list")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Elettronica e Casa create nel setup

@pytest.mark.asyncio
async def test_update_category(client):
    """Test E2E: Aggiornamento nome categoria."""
    # Aggiorniamo la categoria 1 (Elettronica)
    response = await client.put("/categories/update/1", json={"name": "Tech"})
    assert response.status_code == 200
    assert response.json()["name"] == "Tech"

@pytest.mark.asyncio
async def test_delete_category_fail(client):
    """Test E2E: Tentativo di eliminazione di categoria con prodotti associati (deve fallire)."""
    # La categoria 1 ha dei prodotti, quindi il delete deve ritornare 400
    response = await client.delete("/categories/delete/1")
    assert response.status_code == 400
    assert "prodotti associati" in response.json()["detail"]