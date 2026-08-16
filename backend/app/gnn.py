# Optional PyTorch Geometric scaffold.
# The default application intentionally does not require PyG.
# Install backend/requirements-optional.txt to use this module.

def build_pyg_data(nodes, edges):
    try:
        import torch
        from torch_geometric.data import Data
    except ImportError as exc:
        raise RuntimeError(
            "Install optional dependencies with: "
            "pip install -r requirements-optional.txt"
        ) from exc

    node_ids = {node["id"]: i for i, node in enumerate(nodes)}
    x = torch.tensor(
        [[float(n.get("risk", 0.0)) / 100.0] for n in nodes],
        dtype=torch.float,
    )
    edge_index = torch.tensor(
        [
            [node_ids[e["source"]] for e in edges],
            [node_ids[e["target"]] for e in edges],
        ],
        dtype=torch.long,
    )
    return Data(x=x, edge_index=edge_index)
