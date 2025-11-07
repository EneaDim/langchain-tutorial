from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from smart_report_writer.core.models.settings import AppSettings

def get_engine(settings: AppSettings):
    url = f"postgresql+psycopg://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    return create_engine(url, pool_pre_ping=True)

def get_sessionmaker(engine):
    return sessionmaker(bind=engine, expire_on_commit=False, autocommit=False, autoflush=False)
