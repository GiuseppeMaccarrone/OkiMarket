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
    # Questo test ORA passerà perché confermiamo che Pydantic deve sollevare ValidationError
    with pytest.raises(ValidationError):
        CategoryCreate(**data)

# Se aggiungi altri campi in futuro (es. descrizione),
# aggiungi qui i test per la validazione di quei campi!