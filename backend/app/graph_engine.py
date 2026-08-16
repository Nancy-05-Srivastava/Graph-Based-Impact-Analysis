import json
from pathlib import Path
from typing import Dict, List
import networkx as nx

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "synthetic_bank_360.json"

class FRDGEngine:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.load_demo_graph()

    def load_demo_graph(self):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        for node in data["nodes"]:
            self.graph.add_node(**node)
        for edge in data["edges"]:
            self.graph.add_edge(
                edge["source"], edge["target"],
                relation=edge["relation"], weight=edge.get("weight", 1.0)
            )

    def graph_json(self):
        return {
            "nodes": [
                {
                    "id": node_id,
                    "label": attrs.get("label", node_id),
                    "type": attrs.get("type", "Unknown"),
                    "risk": float(attrs.get("risk", 0.0)),
                    "metadata": attrs.get("metadata", {}),
                }
                for node_id, attrs in self.graph.nodes(data=True)
            ],
            "edges": [
                {
                    "source": s, "target": t,
                    "relation": a.get("relation", "depends_on"),
                    "weight": float(a.get("weight", 1.0)),
                }
                for s, t, a in self.graph.edges(data=True)
            ],
        }

    def infer_source(self, topics: List[str]) -> str:
        topic_map = {
            "payment": "reg_cross_border",
            "cross_border": "reg_cross_border",
            "kyc": "reg_kyc",
            "aml": "reg_aml",
            "sanctions": "reg_sanctions",
            "data": "reg_data",
        }
        for topic in topics:
            if topic in topic_map and topic_map[topic] in self.graph:
                return topic_map[topic]
        return "reg_cross_border"

    def impact(self, source_id: str, max_depth: int = 5):
        if source_id not in self.graph:
            raise KeyError(source_id)

        impacted = []
        paths = []

        for target in self.graph.nodes:
            if target == source_id:
                continue
            try:
                path = nx.shortest_path(self.graph, source_id, target)
            except nx.NetworkXNoPath:
                continue

            distance = len(path) - 1
            if 1 <= distance <= max_depth:
                attrs = self.graph.nodes[target]
                risk = min(100.0, float(attrs.get("risk", 0.0)) + self._path_risk(path))
                impacted.append({
                    "node_id": target,
                    "label": attrs.get("label", target),
                    "type": attrs.get("type", "Unknown"),
                    "risk": round(risk, 1),
                    "distance": distance,
                    "path": path,
                })
                if len(path) >= 3 and len(paths) < 8:
                    paths.append(path)

        impacted.sort(key=lambda x: (-x["risk"], x["distance"]))
        counts: Dict[str, int] = {}
        for item in impacted:
            counts[item["type"]] = counts.get(item["type"], 0) + 1

        source_risk = float(self.graph.nodes[source_id].get("risk", 0.0))
        max_risk = max([x["risk"] for x in impacted], default=source_risk)
        return impacted, counts, paths, round(max_risk, 1)

    def _path_risk(self, path: List[str]) -> float:
        score = 0.0
        for i, node_id in enumerate(path[1:], start=1):
            node_risk = float(self.graph.nodes[node_id].get("risk", 0.0))
            score += node_risk * (0.18 ** (i - 1))
        return min(70.0, score)
