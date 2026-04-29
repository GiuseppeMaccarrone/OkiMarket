from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from pydantic import BaseModel, ConfigDict, Field, field_validator
from config.database import BaseAlchemy

# ==========================================
# SCHEMI PYDANTIC (Validazione e API)
# ==========================================

class CategoryCreate(BaseModel):
    # Validiamo la lunghezza: minimo 2 caratteri, massimo 100
    name: str = Field(..., min_length=2, max_length=100)

    @field_validator('name')
    @classmethod
    def clean_name(cls, v: str) -> str:
        # Pulisce spazi, converte in formato leggibile (es: "Elettronica")
        # .strip() rimuove spazi, .capitalize() rende la prima lettera maiuscola
        cleaned = v.strip()
        if not cleaned:
            raise ValueError('Il nome della categoria non può essere vuoto')
        return cleaned.capitalize()

    model_config = ConfigDict(from_attributes=True)


class Category(CategoryCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# MODELLI SQLALCHEMY (Database)
# ==========================================

class CategoryModelAlchemy(BaseAlchemy):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Impostiamo una lunghezza massima anche nel DB per coerenza con Pydantic
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    # Relazione: Una categoria ha molti prodotti
    # Il cascade="all, delete-orphan" è utile se vuoi che eliminando la categoria
    # si gestisca la relazione, ma attenzione al RESTRICT che hai nel prodotto!
    products: Mapped[list["ProductModelAlchemy"]] = relationship(
        "ProductModelAlchemy", back_populates="category"
    )