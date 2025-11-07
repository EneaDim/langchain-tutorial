from sqlalchemy import text
from sqlalchemy.orm import Session
from smart_report_writer.core.models.domain import Document, ContentKind
from typing import Any, Dict

class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(self, filename: str, mime: str | None, content_kind: ContentKind, size_bytes: int, sha256: str, extra: Dict[str, Any]) -> Document:
        # minimal insert via raw SQL for brevity
        sql = text("INSERT INTO documents (id, filename, mime, content_kind, size_bytes, sha256, extra) VALUES (gen_random_uuid(), :f, :m, :ck, :sz, :h, :e) RETURNING id, filename, mime, content_kind, size_bytes, sha256, extra, created_at")
        row = self.db.execute(sql, {"f": filename, "m": mime, "ck": content_kind.value, "sz": size_bytes, "h": sha256, "e": extra}).first()
        self.db.commit()
        return Document(id=row.id, filename=row.filename, mime=row.mime, content_kind=ContentKind(row.content_kind), size_bytes=row.size_bytes, sha256=row.sha256, extra=row.extra, created_at=row.created_at)
