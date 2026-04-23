import os
from testcontainers.postgres import PostgresContainer
from models.product import BaseAlchemy
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import delete
from models.product import ProductModelAlchemy
from models.category import CategoryModelAlchemy


# ==========================================
# FIXTURE DI SETUP: Crea i dati per i test
# ==========================================

@pytest.fixture(scope="function", autouse=True)
async def setup_catalog(postgres_url):
    # Usiamo una fixture asincrona nativa (niente asyncio.run)
    test_engine = create_async_engine(postgres_url, poolclass=NullPool)
    TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

    async with TestingSessionLocal() as session:
        # Pulisci
        await session.execute(delete(ProductModelAlchemy))
        await session.execute(delete(CategoryModelAlchemy))
        await session.commit()

        # Crea Categorie
        cat_elettronica = CategoryModelAlchemy(name="Elettronica")
        cat_casa = CategoryModelAlchemy(name="Casa")
        session.add_all([cat_elettronica, cat_casa])
        await session.commit()
        await session.refresh(cat_elettronica)
        await session.refresh(cat_casa)

        # Crea Prodotti
        p1 = ProductModelAlchemy(name="Mouse Economico", price=10.00, category_id=cat_elettronica.id)
        p2 = ProductModelAlchemy(name="Tastiera Meccanica", price=80.00, category_id=cat_elettronica.id)
        p3 = ProductModelAlchemy(name="Monitor 4K", price=300.00, category_id=cat_casa.id)
        session.add_all([p1, p2, p3])
        await session.commit()

    await test_engine.dispose()


# ==========================================
# 1. IL DATABASE: scope="function"
# Usiamo 'def' normale per aggirare lo ScopeMismatch di pytest-asyncio
# ==========================================
@pytest.fixture(scope="function")
def postgres_url():
    with PostgresContainer("postgres:16-alpine") as postgres:
        url = postgres.get_connection_url().replace("postgresql+psycopg2", "postgresql+asyncpg")
        os.environ["DATABASE_URL"] = url

        # Creiamo una micro-funzione asincrona solo per la creazione delle tabelle
        async def init_db():
            engine = create_async_engine(url, poolclass=NullPool)
            async with engine.begin() as conn:
                await conn.run_sync(BaseAlchemy.metadata.create_all)
            await engine.dispose()

        # Eseguiamo la creazione in modo "protetto" e isolato
        asyncio.run(init_db())

        yield url


# ==========================================
# 2. IL CLIENT: scope="function" (ASINCRONA)
# Questo va benissimo ad async def perché è scope="function" (il default per i test)
# ==========================================
@pytest.fixture(scope="function")
async def client(postgres_url):
    test_engine = create_async_engine(postgres_url, poolclass=NullPool)
    TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

    import services.product_service
    services.product_service.AsyncSessionLocal = TestingSessionLocal

    import services.category_service
    services.category_service.AsyncSessionLocal = TestingSessionLocal

    from main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as ac:
        yield ac

    await test_engine.dispose()