import asyncio
from logging.config import fileConfig
import sys
import os

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. IMPORTANTE: Aggiungiamo il path per trovare i moduli (se non bastasse il Source Root dell'IDE)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 2. IMPORTA LA BASE E I MODELLI (Serve per popolare i metadati)
from config.database import get_db_url, BaseAlchemy
from models.category import CategoryModelAlchemy
from models.product import ProductModelAlchemy

# Accesso alla configurazione di Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. SETTA I METADATI (Ora Alembic "vede" le tabelle)
target_metadata = BaseAlchemy.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Traduciamo 'db' in 'localhost' per Windows
    url = get_db_url().replace("@db:5432", "@localhost:5432")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine..."""

    # Prendiamo la sezione dal file .ini
    config_section = config.get_section(config.config_ini_section, {})

    # 4. INJETTIAMO L'URL REALE (Sostituisce il placeholder nel file .ini)
    # Traduciamo anche qui 'db' in 'localhost' per il terminale locale
    config_section["sqlalchemy.url"] = get_db_url().replace("@db:5432", "@localhost:5432")

    connectable = async_engine_from_config(
        config_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()