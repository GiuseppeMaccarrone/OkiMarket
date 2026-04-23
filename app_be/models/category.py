from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, ConfigDict
from models.product import BaseAlchemy

# ==========================================
# SCHEMI PYDANTIC (Validazione e API)
# ==========================================

class CategoryCreate(BaseModel):
    name: str

class Category(CategoryCreate):
    id: int

    # Permette a Pydantic di leggere l'oggetto SQLAlchemy e trasformarlo in JSON
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# MODELLI SQLALCHEMY (Database)
# ==========================================

class CategoryModelAlchemy(BaseAlchemy):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Relazione: Una categoria ha molti prodotti
    products: Mapped[list["ProductModelAlchemy"]] = relationship(
        "ProductModelAlchemy", back_populates="category"
    )