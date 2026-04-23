
from models.product import ProductQueryParams

import pytest
from pydantic import ValidationError
from models.product import ProductCreate, Product

def test_product_model_from_attributes():
    # Simuliamo un oggetto ORM (o un dict) che viene convertito nel modello Product
    # Questo testa la logica "from_attributes = True"
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
