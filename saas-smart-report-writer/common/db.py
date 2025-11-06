from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

engine = create_engine(settings.postgres_dsn, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()
