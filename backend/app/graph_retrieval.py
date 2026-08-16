from typing import List

from .graph_engine import FRDGEngine


class GraphRAGRetriever:
    """Small, explainable graph-grounded retrieval layer for the prototype.

    It retrieves the highest-risk dependency paths around a regulatory node.
    This is intentionally transparent; an embedding/vector retriever can be
    added later without changing the FRDG data model.
    """

    def __init__(self, engine: FRDGEngine):
        self.engine = engine

    def retrieve(self, source_id: str, limit: int = 8) -> List[dict]:
        impacted, _, paths, _ = self.engine.impact(source_id)
        by_id = {x["node_id"]: x for x in impacted}
        evidence = []
        for path in paths[:limit]:
            evidence.append({
                "path": path,
                "risk": max((by_id.get(n, {}).get("risk", 0) for n in path), default=0),
            })
        return evidence
