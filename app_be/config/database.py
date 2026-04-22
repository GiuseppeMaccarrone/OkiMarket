import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Definiamo la base per i tuoi modelli
BaseAlchemy = declarative_base()

def get_db_url():
    """
    Legge l'URL dal sistema.
    Se è impostato DATABASE_URL (es. dai test), usa quello.
    Altrimenti usa quello di default per il container Docker.
    """
    return os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://admin:password_segreta@db:5432/catalogo_db"
    )

# Creiamo l'engine in modo che legga sempre l'url aggiornato
def get_engine():
    return create_async_engine(get_db_url(), echo=False)

# Sessione che il tuo Service userà
AsyncSessionLocal = async_sessionmaker(
    bind=get_engine(),
    expire_on_commit=False
)