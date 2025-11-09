from pydantic import BaseModel, Field
from typing import List

class AnalyzeResult(BaseModel):
    pages: int = Field(ge=0)
    summary: str
    keywords: List[str]

class JobOut(BaseModel):
    id: int
    filename: str
    summary: str
