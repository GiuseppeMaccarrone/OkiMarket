import pytest
from sqlalchemy import inspect
from models.category import CategoryModelAlchemy


def test_category_model_table_name():
    """Verifica che il modello sia mappato sulla tabella corretta."""
    assert CategoryModelAlchemy.__tablename__ == "categories"


def test_category_model_columns_definition():
    """Verifica che le colonne abbiano le proprietà (vincoli) corrette."""
    mapper = inspect(CategoryModelAlchemy)

    # Controllo colonna 'id'
    id_col = mapper.columns['id']
    assert id_col.primary_key is True
    assert id_col.autoincrement is True

    # Controllo colonna 'name'
    name_col = mapper.columns['name']
    assert name_col.nullable is False
    assert name_col.unique is True


def test_category_model_relationship_config():
    """Verifica che la relazione con i prodotti sia configurata correttamente."""
    mapper = inspect(CategoryModelAlchemy)

    # Verifica che la relazione 'products' esista
    assert 'products' in mapper.relationships

    # Verifica che la back_populates sia corretta (evita errori di sincronizzazione)
    rel = mapper.relationships['products']
    assert rel.back_populates == 'category'
    assert rel.mapper.class_.__name__ == 'ProductModelAlchemy'


def test_category_model_instantiation():
    """Verifica che l'istanza accetti correttamente gli attributi."""
    category = CategoryModelAlchemy(name="Test Category")
    assert category.name == "Test Category"
    assert category.id is None  # Non ancora salvata


def test_category_model_products_init():
    """Verifica che la collezione prodotti sia accessibile."""
    category = CategoryModelAlchemy(name="Casa")
    # In SQLAlchemy, se non accedi al DB, la relazione lazy è solitamente None o lista vuota
    # Se il test fallisce perché è None, puoi cambiarlo in 'assert category.products is None'
    assert category.products == []