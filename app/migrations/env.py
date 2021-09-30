import logging
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from dynaconf import Dynaconf, Validator
from sqlalchemy import engine_from_config, pool

from app.services.db import models


# LOGGER
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# CORE SETTINGS
settings = Dynaconf(
    envvar_prefix=False,
    validators=[
        # DATABASE
        Validator(
            "DB_CONFIG.DB_HOST",
            "DB_CONFIG.DB_NAME",
            "DB_CONFIG.DB_USER",
            must_exist=True,
            is_type_of=str,
        ),
        Validator("DB_CONFIG.DB_PORT", must_exist=True, is_type_of=int),
        Validator("DB_CONFIG.DB_PASS", must_exist=True, is_type_of=str)
        | Validator("DB_CONFIG.DB_PASS", must_exist=True, is_type_of=int),
    ],
    environments=True,
    settings_files=["settings.toml"],
)


# DB CONNECT
DB_HOST = settings.DB_CONFIG.DB_HOST
DB_PORT = settings.DB_CONFIG.DB_PORT
DB_USER = settings.DB_CONFIG.DB_USER
DB_NAME = settings.DB_CONFIG.DB_NAME
DB_PASS = settings.DB_CONFIG.DB_PASS

config = context.config

config.set_main_option(
    "sqlalchemy.url", f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = models.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
