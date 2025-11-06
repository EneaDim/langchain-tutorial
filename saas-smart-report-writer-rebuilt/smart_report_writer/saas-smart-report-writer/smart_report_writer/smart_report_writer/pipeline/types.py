from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Any, Dict, List
import pandas as pd

@dataclass
class LoadedDoc:
    path: str
    mimetype: Optional[str]
    text: str
    tables: List[pd.DataFrame] = field(default_factory=list)

@dataclass
class SummaryContext:
    topic: Optional[str]
    docs: List[LoadedDoc]
    combined_text: str
    table_stats: List[Dict[str, Any]]
    llm_sections: Dict[str, str]
