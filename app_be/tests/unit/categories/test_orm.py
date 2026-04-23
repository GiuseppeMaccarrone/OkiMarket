from models.category import CategoryModelAlchemy


# --- TEST SU CATEGORY MODEL (STRUTTURA ORM) ---

def test_category_model_attributes():
    """Verifica che il modello ORM abbia i campi corretti."""
    category = CategoryModelAlchemy(id=1, name="Elettronica")

    assert category.id == 1
    assert category.name == "Elettronica"


def test_category_model_relationship_initialization():
    """Verifica che la lista dei prodotti sia inizializzata (anche se vuota)."""
    category = CategoryModelAlchemy(name="Casa")

    # La relazione 'products' dovrebbe essere inizializzata come lista vuota
    # o accessibile se non definita, a seconda della configurazione SQLAlchemy
    assert category.products == []


def test_category_model_table_name():
    """Verifica che il nome della tabella nel DB sia quello corretto."""
    assert CategoryModelAlchemy.__tablename__ == "categories"