from pydantic import BaseModel, Field
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4
from datetime import datetime

class ContentKind(str, Enum):
    document = "document"
    tabular = "tabular"
    code = "code"
    media = "media"
    email = "email"
    archive = "archive"

class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    filename: str
    mime: str | None = None
    content_kind: ContentKind
    size_bytes: int
    sha256: str
    extra: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
