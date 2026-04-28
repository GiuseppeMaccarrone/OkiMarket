import pytest
from pydantic import ValidationError
from models.product import Product
from datetime import datetime, timezone


def test_product_model_full_image_url_logic():
    """Verifica la logica del campo calcolato full_image_url."""
    # Aggiungiamo un created_at valido per soddisfare Pydantic
    now = datetime.now(timezone.utc)

    # Caso 1: immagine presente
    p1 = Product(
        id=1,
        name="P1",
        price=10.0,
        category_id=1,
        image_url="custom.png",
        created_at=now
    )
    assert p1.full_image_url == "custom.png"

    # Caso 2: immagine assente (usa default)
    p2 = Product(
        id=2,
        name="P2",
        price=10.0,
        category_id=1,
        image_url=None,
        created_at=now
    )
    assert p2.full_image_url == "/static/images/default-product.png"


def test_product_model_from_attributes():
    """Test standard: converte correttamente i dati del DB nel modello Pydantic."""
    data = {
        "id": 1,
        "name": "Prodotto DB",
        "price": 20.0,
        "category_id": 2,
        "tags": ["tag1"],
        "created_at": "2026-04-21T10:00:00"
    }
    product = Product.model_validate(data)
    assert product.id == 1
    assert product.name == "Prodotto DB"


def test_product_model_invalid_id_type():
    """Verifica che il modello rifiuti un ID non convertibile in intero."""
    data = {
        "id": "non-un-id",
        "name": "Prodotto",
        "price": 10.0,
        "category_id": 1,
        "created_at": datetime.now()
    }
    with pytest.raises(ValidationError):
        Product.model_validate(data)


def test_product_model_missing_required_orm_fields():
    """Verifica che il modello rifiuti dati che mancano di campi essenziali del DB (es. id)."""
    data = {
        "name": "Prodotto senza ID",
        "price": 10.0,
        "category_id": 1,
        "created_at": datetime.now()
    }
    # Product richiede 'id', ProductCreate no. Se proviamo a validare un 'Product' senza id, deve fallire.
    with pytest.raises(ValidationError):
        Product.model_validate(data)


def test_product_model_invalid_datetime():
    """Verifica che il modello rifiuti una data malformata."""
    data = {
        "id": 1,
        "name": "Prodotto",
        "price": 10.0,
        "category_id": 1,
        "created_at": "questa-non-è-una-data"
    }
    with pytest.raises(ValidationError):
        Product.model_validate(data)


def test_product_model_full_image_url_logic():
    """Verifica la logica del campo calcolato full_image_url."""
    # Aggiungiamo un created_at valido per soddisfare Pydantic
    now = datetime.now(timezone.utc)

    # Caso 1: immagine presente
    p1 = Product(
        id=1,
        name="P1",
        price=10.0,
        category_id=1,
        image_url="custom.png",
        created_at=now
    )
    assert p1.full_image_url == "custom.png"

    # Caso 2: immagine assente (usa default)
    p2 = Product(
        id=2,
        name="P2",
        price=10.0,
        category_id=1,
        image_url=None,
        created_at=now
    )
    assert p2.full_image_url == "/static/images/default-product.png"