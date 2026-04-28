import os
import pytest
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import delete

# Importiamo direttamente i modelli
from models.product import ProductModelAlchemy
from models.category import CategoryModelAlchemy

def pytest_collection_modifyitems(items):
    """
    Ordina i test in modo che quelli nella cartella 'unit' vengano eseguiti per primi.
    """
    items.sort(key=lambda x: "unit" not in x.nodeid)

# ==========================================
# 1. IL DATABASE: scope="function" (ASYNC)
# ==========================================
@pytest.fixture(scope="function")
async def postgres_url():
    # TRUCCO: Ora la fixture è 'async def'.
    # Così facendo, rimaniamo nello STESSO event loop dei test (addio asyncio.run!)
    with PostgresContainer("postgres:16-alpine") as postgres:
        url = postgres.get_connection_url().replace("postgresql+psycopg2", "postgresql+asyncpg")
        os.environ["DATABASE_URL"] = url

        # Inizializziamo le tabelle qui dentro
        engine = create_async_engine(url, poolclass=NullPool)
        async with engine.begin() as conn:
            # Creiamo esplicitamente le tabelle per entrambi i modelli.
            # Questo bypassa il bisogno di avere un BaseAlchemy centralizzato!
            await conn.run_sync(CategoryModelAlchemy.metadata.create_all)
            await conn.run_sync(ProductModelAlchemy.metadata.create_all)
        await engine.dispose()

        yield url

# ==========================================
# 2. FIXTURE DI SETUP: Crea i dati per i test
# ==========================================
@pytest.fixture(scope="function", autouse=True)
async def setup_catalog(postgres_url):
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
# 3. IL CLIENT: scope="function" (ASYNC)
# ==========================================
@pytest.fixture(scope="function")
async def client(postgres_url):
    test_engine = create_async_engine(postgres_url, poolclass=NullPool)
    TestingSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

    # Patch per i service: rimane fedele al tuo codice
    import services.product_service
    services.product_service.AsyncSessionLocal = TestingSessionLocal

    import services.category_service
    services.category_service.AsyncSessionLocal = TestingSessionLocal

    # FIX per il MaxRetryError di MinIO quando gira in Docker
    if os.path.exists("/.dockerenv") or os.environ.get("DOCKER_ENV"):
        os.environ["MINIO_ENDPOINT"] = "minio:9000"

    from main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test/api/v1") as ac:
        yield ac

    await test_engine.dispose()