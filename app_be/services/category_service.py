
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.category import CategoryModelAlchemy, CategoryCreate, Category
from services.product_service import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryService:

    @staticmethod
    async def create_category(category_in: CategoryCreate) -> Category:
        async with AsyncSessionLocal() as session:
            new_category = CategoryModelAlchemy(name=category_in.name)
            session.add(new_category)
            try:
                await session.commit()
                await session.refresh(new_category)
                return Category.model_validate(new_category)
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome categoria già esistente")

    @staticmethod
    async def list_categories() -> list[Category]:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(CategoryModelAlchemy))
            categories = result.scalars().all()
            return [Category.model_validate(cat) for cat in categories]

    @staticmethod
    async def get_category(category_id: int) -> Category:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(CategoryModelAlchemy).where(CategoryModelAlchemy.id == category_id))
            category = result.scalar_one_or_none()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria non trovata")
            return Category.model_validate(category)

    @staticmethod
    async def update_category(category_id: int, category_in: CategoryCreate) -> Category:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(CategoryModelAlchemy).where(CategoryModelAlchemy.id == category_id))
            category = result.scalar_one_or_none()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria non trovata")

            category.name = category_in.name
            try:
                await session.commit()
                await session.refresh(category)
                return Category.model_validate(category)
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome categoria già esistente")

    @staticmethod
    async def delete_category(category_id: int) -> dict:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(CategoryModelAlchemy).where(CategoryModelAlchemy.id == category_id))
            category = result.scalar_one_or_none()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria non trovata")

            try:
                await session.delete(category)
                await session.commit()
                return {"message": "Categoria eliminata con successo"}
            except IntegrityError:
                await session.rollback()
                # QUESTO È FONDAMENTALE: Impedisce al DB di crashare se elimini una categoria piena!
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Impossibile eliminare: ci sono ancora prodotti associati a questa categoria."
                )
