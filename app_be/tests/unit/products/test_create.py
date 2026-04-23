
import pytest
from pydantic import ValidationError
from models.product import ProductCreate, Product

# --- TEST SU PRODUCT CREATE (VALIDAZIONE INPUT) ---

def test_product_create_valid():
    data = {"name": "Test", "price": 10.0, "category_id": 1}
    product = ProductCreate(**data)
    assert product.name == "Test"
    assert product.price == 10.0

def test_product_create_negative_price():
    data = {"name": "Test", "price": -1.0, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)

def test_product_create_missing_required_fields():
    # Testiamo che manchino campi obbligatori (es. category_id)
    data = {"name": "Test", "price": 10.0}
    with pytest.raises(ValidationError):
        ProductCreate(**data)

def test_product_create_invalid_types():
    # Testiamo un tipo errato (prezzo passato come stringa che non è un numero)
    data = {"name": "Test", "price": "non-un-numero", "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)

def test_product_create_empty_tags():
    # Verifichiamo che il default sia una lista vuota
    data = {"name": "Test", "price": 10.0, "category_id": 1}
    product = ProductCreate(**data)
    assert product.tags == []

def test_product_create_with_tags():
    data = {"name": "Test", "price": 10.0, "category_id": 1, "tags": ["tech", "sale"]}
    product = ProductCreate(**data)
    assert len(product.tags) == 2
    assert "tech" in product.tags