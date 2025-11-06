import uuid, json, datetime as dt
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from common.db import Base, init_db

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    org_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="queued")
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow)
    updated_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)
    sources: Mapped[str] = mapped_column(Text)         # JSON list
    template: Mapped[str | None] = mapped_column(String, nullable=True)
    artifacts: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON list of URLs
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    @staticmethod
    def new(org_id: str, sources: list[str], template: str | None):
        j = Job(org_id=org_id, sources=json.dumps(sources), template=template)
        return j

    @property
    def sources_list(self): return json.loads(self.sources or "[]")
    @property
    def artifacts_list(self): return json.loads(self.artifacts or "[]")
    @artifacts_list.setter
    def artifacts_list(self, v): self.artifacts = json.dumps(v)

init_db()
