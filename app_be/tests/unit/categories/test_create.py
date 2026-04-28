import pytest
from pydantic import ValidationError
from models.category import CategoryCreate

# --- TEST SU CATEGORY CREATE (VALIDAZIONE INPUT) ---

def test_category_create_valid():
    """Test creazione categoria valida."""
    data = {"name": "Elettronica"}
    category = CategoryCreate(**data)
    assert category.name == "Elettronica"

def test_category_create_missing_name():
    """Test che la creazione fallisca se il nome è mancante."""
    data = {}
    with pytest.raises(ValidationError):
        CategoryCreate(**data)

def test_category_create_invalid_name_type():
    """Test che il nome debba essere una stringa."""
    data = {"name": 12345}
    with pytest.raises(ValidationError):
        CategoryCreate(**data)

def test_category_create_too_short():
    """Test nome troppo corto (min_length=2)."""
    with pytest.raises(ValidationError) as exc:
        CategoryCreate(name="A")
    assert "String should have at least 2 characters" in str(exc.value)

def test_category_create_too_long():
    """Test nome troppo lungo (max_length=100)."""
    with pytest.raises(ValidationError) as exc:
        CategoryCreate(name="a" * 101)
    assert "String should have at most 100 characters" in str(exc.value)

def test_category_create_blank_name():
    """Test nome composto solo da spazi."""
    with pytest.raises(ValidationError) as exc:
        CategoryCreate(name="   ")
    assert "Il nome della categoria non può essere vuoto" in str(exc.value)

def test_category_create_normalization():
    """Test che il validatore pulisca gli spazi e capitalizzi."""
    data = {"name": "  elettronica  "}
    category = CategoryCreate(**data)
    assert category.name == "Elettronica"

def test_category_create_boundary_length():
    """Test bordo: nome di esattamente 2 caratteri (valido)."""
    data = {"name": "Tv"}
    category = CategoryCreate(**data)
    assert category.name == "Tv"