from typing import List, Optional
from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, ARRAY, DateTime
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from datetime import datetime, timezone
from config.database import BaseAlchemy

# ==========================================
# SCHEMI PYDANTIC (Validazione e API)
# ==========================================

class ProductSortBy(str, Enum):
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"


class ProductCreate(BaseModel):
    # Validazione nome: non vuoto e massimo 255 caratteri
    name: str = Field(..., min_length=1, max_length=255)
    price: float = Field(..., gt=0)
    category_id: int = Field(..., gt=0)
    tags: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    image_url: Optional[str] = Field(None, max_length=512)

    # Validatore personalizzato per pulire il nome
    @field_validator('name')
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Il nome non può essere solo spazi bianchi')
        return v.strip()

    model_config = ConfigDict(from_attributes=True)


class Product(ProductCreate):
    id: int
    created_at: datetime

    @property
    def full_image_url(self) -> str:
        return self.image_url or "/static/images/default-product.png"

    model_config = ConfigDict(from_attributes=True)


class ProductQueryParams(BaseModel):
    search: Optional[str] = None
    category_id: Optional[int] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    sort_by: ProductSortBy = ProductSortBy.CREATED_AT_DESC
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

    @model_validator(mode='after')
    def validate_price_range(self):
        if self.min_price is not None and self.max_price is not None:
            if self.min_price > self.max_price:
                raise ValueError("min_price non può essere maggiore di max_price")
        return self


# ==========================================
# MODELLI SQLALCHEMY (Database)
# ==========================================

class ProductModelAlchemy(BaseAlchemy):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"))
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=[])

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    category: Mapped["CategoryModelAlchemy"] = relationship(
        "CategoryModelAlchemy", back_populates="products"
    )