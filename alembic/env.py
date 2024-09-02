from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.models import Base  # Import your models' Base
from dotenv import load_dotenv  # Import dotenv to load .env
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Provide the MetaData object for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL  # Use the URL loaded from the environment
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()




# # alembic/env.py

# from logging.config import fileConfig
# from sqlalchemy import engine_from_config
# from sqlalchemy import pool
# from alembic import context

# # Import your SQLAlchemy models and the Base
# from app.models import Base  # Ensure this is correctly imported
# from app.database import DATABASE_URL  # Use the correct DATABASE_URL from your config

# # This is the Alembic Config object, which provides access to the values within the .ini file in use.
# config = context.config

# # Interpret the config file for Python logging.
# # This line sets up loggers basically.
# fileConfig(config.config_file_name)

# # Provide the MetaData object for 'autogenerate' support
# target_metadata = Base.metadata  # Ensure this is correctly set

# def run_migrations_online():
#     """Run migrations in 'online' mode."""
#     connectable = engine_from_config(
#         config.get_section(config.config_ini_section),
#         prefix="sqlalchemy.",
#         poolclass=pool.NullPool,
#         url=DATABASE_URL  # Ensure the URL is correctly set
#     )

#     with connectable.connect() as connection:
#         context.configure(
#             connection=connection,
#             target_metadata=target_metadata,  # Pass the target metadata here
#             compare_type=True  # Optionally enable type comparison
#         )

#         with context.begin_transaction():
#             context.run_migrations()

# run_migrations_online()