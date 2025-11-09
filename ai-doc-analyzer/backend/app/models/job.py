from sqlalchemy import Column, Integer, String, Text
from app.models.db import Base

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    keywords = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
