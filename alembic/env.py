import os
import sys
from logging.config import fileConfig
from os.path import abspath, dirname

from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from alembic import context

# Add project root to path
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# Import models
from app.models.user import User

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def get_url():
    # اولویت با متغیر محیطی است
    return os.getenv("DATABASE_URL")

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


def run_migrations_online() -> None:
    url = get_url()
    if not url:
        raise ValueError("No DATABASE_URL found in environment variables")

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = url
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()