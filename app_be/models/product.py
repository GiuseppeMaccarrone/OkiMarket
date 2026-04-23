from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, ForeignKey, ARRAY
from datetime import datetime


# --- Pydantic --- #
class ProductSortBy(str, Enum):
    PRICE_ASC = "price_asc"
    PRICE_DESC = "price_desc"
    CREATED_AT_ASC = "created_at_asc"
    CREATED_AT_DESC = "created_at_desc"


class ProductCreate(BaseModel):
    name: str
    price: float = Field(..., ge=0)
    category_id: int
    tags: List[str] = []
    created_at: Optional[datetime] = datetime.now()
    image_url: Optional[str] = None  # Opzionale


class Product(ProductCreate):
    id: int
    created_at: datetime

    @property
    def full_image_url(self) -> str:
        return self.image_url or "/static/images/default-product.png"

    class Config:
        from_attributes = True


class ProductQueryParams(BaseModel):
    search: Optional[str] = None
    category_id: Optional[int] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    sort_by: ProductSortBy = ProductSortBy.CREATED_AT_DESC
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)

# --- Sql Alchemy --- #
class BaseAlchemy(DeclarativeBase):
    pass

class ProductModelAlchemy(BaseAlchemy):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"))
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=[])
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    image_url: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)

    category: Mapped["CategoryModelAlchemy"] = relationship(
        "CategoryModelAlchemy", back_populates="products"
    )