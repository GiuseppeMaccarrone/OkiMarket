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


# ==========================================
# FIXTURE DI SETUP: Crea i dati per i test
# ==========================================

@pytest.fixture(autouse=True, scope="module")
def setup_catalog(postgres_url):
    """
    Svuota il database e lo popola con esattamente 3 prodotti.
    """

    async def _seed_db():
        test_engine = create_async_engine(postgres_url, poolclass=NullPool)
        TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

        # 1. 🔥 PULIZIA TOTALE: Svuotiamo la tabella dei prodotti
        async with TestingSessionLocal() as session:
            await session.execute(delete(ProductModelAlchemy))
            await session.commit()

        # Patch sul servizio
        import services.product_service
        services.product_service.AsyncSessionLocal = TestingSessionLocal
        from main import app

        # 2. Inseriamo i 3 prodotti base
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as ac:
            await ac.post("/products/create", json={
                "name": "Mouse Economico", "price": 10.00, "category_id": 1, "tags": []
            })
            await ac.post("/products/create", json={
                "name": "Tastiera Meccanica", "price": 80.00, "category_id": 1, "tags": []
            })
            await ac.post("/products/create", json={
                "name": "Monitor 4K", "price": 300.00, "category_id": 2, "tags": []
            })

        await test_engine.dispose()

    asyncio.run(_seed_db())


# ==========================================
# 1. IL DATABASE: scope="session" (ORA SINCRONA)
# Usiamo 'def' normale per aggirare lo ScopeMismatch di pytest-asyncio
# ==========================================
@pytest.fixture(scope="session")
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

    from main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as ac:
        yield ac

    await test_engine.dispose()