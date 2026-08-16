import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.app.graph_engine import FRDGEngine

def test_demo_graph_loads():
    engine = FRDGEngine()
    assert engine.graph.number_of_nodes() > 20
    assert engine.graph.number_of_edges() > 20

def test_impact_propagates():
    engine = FRDGEngine()
    impacted, counts, paths, risk = engine.impact("reg_cross_border")
    assert impacted
    assert counts["Internal Policy"] >= 1
    assert counts["API"] >= 1
    assert paths
    assert risk > 0
