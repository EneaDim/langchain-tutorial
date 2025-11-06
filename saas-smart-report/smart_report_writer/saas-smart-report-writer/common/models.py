from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .db import Base

class Org(Base):
    __tablename__ = "orgs"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("orgs.id"))
    email = Column(String, unique=True, nullable=False)
    is_admin = Column(Boolean, default=False)

class File(Base):
    __tablename__ = "files"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("orgs.id"))
    owner_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    mime = Column(String, nullable=False)
    size = Column(Integer, default=0)
    s3_key = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class Template(Base):
    __tablename__ = "templates"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("orgs.id"))
    owner_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    s3_key = Column(String, nullable=False)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True)
    org_id = Column(String, ForeignKey("orgs.id"))
    owner_id = Column(String, ForeignKey("users.id"))
    status = Column(String, default="queued")  # queued/running/done/error
    topic = Column(String, nullable=True)
    model = Column(String, nullable=True)
    temperature = Column(String, nullable=True)
    per_file_cap = Column(Integer, default=12000)
    total_cap = Column(Integer, default=150000)
    template_id = Column(String, ForeignKey("templates.id"), nullable=True)
    files_json = Column(Text)   # JSON array of file ids
    artifacts_json = Column(Text)  # JSON with URLs/keys
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
