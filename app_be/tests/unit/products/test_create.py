
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

def test_product_create_name_too_short():
    """Il nome deve avere almeno 1 carattere."""
    data = {"name": "", "price": 10.0, "category_id": 1}
    with pytest.raises(ValidationError) as exc:
        ProductCreate(**data)
    assert "string_too_short" in str(exc.value)

def test_product_create_name_too_long():
    """Il nome non può superare 255 caratteri."""
    data = {"name": "a" * 256, "price": 10.0, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)

def test_product_create_price_zero():
    """Il prezzo deve essere strettamente maggiore di zero (gt=0)."""
    data = {"name": "Test", "price": 0.0, "category_id": 1}
    with pytest.raises(ValidationError) as exc:
        ProductCreate(**data)
    assert "Input should be greater than 0" in str(exc.value)

def test_product_create_name_blank_spaces():
    """Verifica che il validatore pulisca il nome (o fallisca se solo spazi)."""
    # Se il validatore usa .strip() e il risultato è vuoto, deve fallire
    data = {"name": "   ", "price": 10.0, "category_id": 1}
    with pytest.raises(ValidationError):
        ProductCreate(**data)

def test_product_create_normalization():
    """Verifica che spazi bianchi eccessivi vengano rimossi dal nome."""
    data = {"name": "  Mouse Gaming  ", "price": 50.0, "category_id": 1}
    product = ProductCreate(**data)
    assert product.name == "Mouse Gaming"

def test_product_create_category_id_invalid():
    """La categoria deve essere un ID positivo."""
    data = {"name": "Test", "price": 10.0, "category_id": -5}
    with pytest.raises(ValidationError):
        ProductCreate(**data)

def test_product_create_tags_limit():
    """Verifica che gestisca liste di tag, anche se Pydantic non ha limiti su len() di default."""
    data = {"name": "Test", "price": 10.0, "category_id": 1, "tags": ["tag1", "tag2"]}
    product = ProductCreate(**data)
    assert len(product.tags) == 2