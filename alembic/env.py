import asyncio
import os
import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlmodel import SQLModel

from alembic import context

sys.path.insert(0, dirname(dirname(abspath(__file__))))

import app.models  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def get_url():
    return os.getenv("DATABASE_URL")


async def run_migrations_online() -> None:
    url = get_url()
    if not url:
        raise ValueError("No DATABASE_URL found in environment variables")

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = url

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_offline() -> None:
    url = get_url()
    if not url:
        raise ValueError("No DATABASE_URL found in environment variables")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
