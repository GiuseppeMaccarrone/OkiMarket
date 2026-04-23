import pytest
from pydantic import ValidationError
from models.product import ProductCreate

def test_product_create_valid():
    data = {"name": "Test", "price": 10.0, "category_id": 1}
    product = ProductCreate(**data)
    assert product.name == "Test"

def test_product_create_invalid_price():
    data = {"name": "Test", "price": -1.0, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)