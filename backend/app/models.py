from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Node(BaseModel):
    id: str
    label: str
    type: str
    risk: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class Edge(BaseModel):
    source: str
    target: str
    relation: str
    weight: float = 1.0

class AnalyzeTextRequest(BaseModel):
    text: str
    source_label: Optional[str] = "Uploaded Regulation"
