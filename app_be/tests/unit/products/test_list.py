
from models.product import ProductQueryParams
from models.product import ProductSortBy, ProductQueryParams

import pytest
from pydantic import ValidationError
from models.product import ProductCreate, Product


def test_query_params_defaults():
    params = ProductQueryParams()
    assert params.skip == 0
    assert params.limit == 10

def test_query_params_invalid_limit():
    # Il limite deve essere <= 100 (le=100 nel Field)
    with pytest.raises(ValidationError):
        ProductQueryParams(limit=101)

def test_query_params_invalid_skip():
    # Lo skip non può essere negativo
    with pytest.raises(ValidationError):
        ProductQueryParams(skip=-1)

def test_query_params_valid_sort():
    # Testiamo un sort valido
    params = ProductQueryParams(sort_by=ProductSortBy.PRICE_ASC)
    assert params.sort_by == "price_asc"

def test_query_params_invalid_sort():
    # Testiamo cosa succede se passiamo un valore non previsto dall'Enum
    with pytest.raises(ValidationError):
        ProductQueryParams(sort_by="invalid_sort_option")

def test_query_params_search_length():
    # Testiamo se possiamo passare una stringa di ricerca lunga
    params = ProductQueryParams(search="smartphone")
    assert params.search == "smartphone"

def test_query_params_price_ranges():
    """Test che i prezzi siano coerenti (min < max)."""
    # Nota: se vuoi validare che min <= max, devi aggiungere un validator nel modello
    params = ProductQueryParams(min_price=100, max_price=200)
    assert params.min_price == 100
    assert params.max_price == 200

def test_query_params_negative_prices():
    """Test che non siano ammessi prezzi negativi."""
    with pytest.raises(ValidationError):
        ProductQueryParams(min_price=-50)

def test_query_params_sort_enum_consistency():
    """Verifica che il valore passato sia esattamente quello dell'Enum."""
    params = ProductQueryParams(sort_by=ProductSortBy.PRICE_ASC)
    assert params.sort_by == ProductSortBy.PRICE_ASC