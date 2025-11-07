from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None  # Using SQLAlchemy ORM-less for brevity

def run_migrations_offline():
    url = os.getenv("DB_URL")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        {"sqlalchemy.url": os.getenv("DB_URL")},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            connection.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS documents (
              id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
              filename TEXT NOT NULL,
              mime TEXT,
              content_kind TEXT,
              size_bytes BIGINT,
              sha256 TEXT,
              extra JSONB,
              created_at TIMESTAMPTZ DEFAULT now()
            );
            """)
            connection.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS jobs (
              id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
              document_id UUID,
              template_id TEXT,
              status TEXT,
              created_at TIMESTAMPTZ DEFAULT now()
            );
            """)
            connection.exec_driver_sql("""
            CREATE TABLE IF NOT EXISTS artifacts (
              id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
              job_id UUID,
              kind TEXT,
              path TEXT,
              url TEXT,
              created_at TIMESTAMPTZ DEFAULT now()
            );
            """)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
