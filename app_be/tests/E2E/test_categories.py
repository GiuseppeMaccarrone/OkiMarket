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

@pytest.mark.asyncio
async def test_create_category_invalid_name(client):
    """Test E2E: Validazione fallita (nome troppo corto)."""
    response = await client.post("/categories/create", json={"name": "A"})
    assert response.status_code == 422  # Pydantic deve bloccarlo

@pytest.mark.asyncio
async def test_update_category_not_found(client):
    """Test E2E: Aggiornamento categoria inesistente."""
    response = await client.put("/categories/update/999", json={"name": "Ghost"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_category_success(client):
    """Test E2E: Creazione e successiva eliminazione di una categoria vuota."""
    # 1. Creiamo una categoria nuova
    new_cat = await client.post("/categories/create", json={"name": "Musica"})
    cat_id = new_cat.json()["id"]

    # 2. La eliminiamo
    response = await client.delete(f"/categories/delete/{cat_id}")
    assert response.status_code == 200

    # 3. Verifichiamo che non esista più
    get_response = await client.get(f"/categories/get/{cat_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_create_duplicate_category(client):
    """Test E2E: Tentativo di creare una categoria già esistente."""
    # "Elettronica" esiste già nel setup_catalog
    response = await client.post("/categories/create", json={"name": "Elettronica"})
    assert response.status_code == 400 # O 409 Conflict, dipende dalla tua implementazione