"""
Graph input for Lab 3 empirical analysis.

Input properties (documented for the report):
  - vertices (V): number of nodes
  - edges (E): number of undirected edges (or directed arcs if directed=True)
  - graph_type: sparse | dense | tree | grid | file
  - directed: whether edges are one-way
  - seed: reproducible random generation
"""

import json
import math
import os
import random
from typing import Any


def build_adjacency_list(num_vertices: int, edges: list[list[int]], directed: bool = False) -> list[list[int]]:
    adj = [[] for _ in range(num_vertices)]
    for u, v in edges:
        if u == v:
            continue
        adj[u].append(v)
        if not directed:
            adj[v].append(u)

    for neighbors in adj:
        neighbors.sort()
    return adj


def load_graph_from_json(path: str) -> tuple[list[list[int]], dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    vertices = int(data["vertices"])
    directed = bool(data.get("directed", False))
    edges = [list(edge) for edge in data["edges"]]
    meta = {
        "vertices": vertices,
        "edges": len(edges),
        "graph_type": data.get("graph_type", "file"),
        "directed": directed,
        "source": path,
    }
    return build_adjacency_list(vertices, edges, directed=directed), meta


def _random_edges(num_vertices: int, num_edges: int, directed: bool, rng: random.Random) -> list[list[int]]:
    edge_set: set[tuple[int, int]] = set()
    max_attempts = num_edges * 20
    attempts = 0

    while len(edge_set) < num_edges and attempts < max_attempts:
        u = rng.randrange(num_vertices)
        v = rng.randrange(num_vertices)
        if u == v:
            attempts += 1
            continue

        if directed:
            key = (u, v)
        else:
            key = (min(u, v), max(u, v))

        edge_set.add(key)
        attempts += 1

    return [[u, v] for u, v in edge_set]


def generate_sparse_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[int]], dict[str, Any]]:
    """Sparse graph: E ~= V (average degree ~ 2)."""
    rng = random.Random(seed)
    num_edges = max(num_vertices - 1, num_vertices)
    edges = _random_edges(num_vertices, num_edges, directed=False, rng=rng)
    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "sparse",
        "directed": False,
        "seed": seed,
    }
    return build_adjacency_list(num_vertices, edges), meta


def generate_dense_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[int]], dict[str, Any]]:
    """Dense graph: E ~= V * log2(V)."""
    rng = random.Random(seed)
    num_edges = min(
        num_vertices * (num_vertices - 1) // 2,
        int(num_vertices * max(2, math.log2(max(num_vertices, 2)))),
    )
    edges = _random_edges(num_vertices, num_edges, directed=False, rng=rng)
    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "dense",
        "directed": False,
        "seed": seed,
    }
    return build_adjacency_list(num_vertices, edges), meta


def generate_tree_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[int]], dict[str, Any]]:
    """Tree: connected acyclic graph, E = V - 1."""
    rng = random.Random(seed)
    edges = []
    for v in range(1, num_vertices):
        parent = rng.randrange(v)
        edges.append([parent, v])

    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "tree",
        "directed": False,
        "seed": seed,
    }
    return build_adjacency_list(num_vertices, edges), meta


def generate_grid_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[int]], dict[str, Any]]:
    """Grid graph: nodes on rows x cols lattice, 4-neighbor connections."""
    side = int(math.sqrt(num_vertices))
    if side * side < num_vertices:
        side += 1

    rows, cols = side, side
    actual_vertices = rows * cols
    edges: list[list[int]] = []

    def index(r: int, c: int) -> int:
        return r * cols + c

    for r in range(rows):
        for c in range(cols):
            node = index(r, c)
            if c + 1 < cols:
                edges.append([node, index(r, c + 1)])
            if r + 1 < rows:
                edges.append([node, index(r + 1, c)])

    meta = {
        "vertices": actual_vertices,
        "edges": len(edges),
        "graph_type": "grid",
        "directed": False,
        "requested_vertices": num_vertices,
    }
    return build_adjacency_list(actual_vertices, edges), meta


GENERATORS = {
    "sparse": generate_sparse_graph,
    "dense": generate_dense_graph,
    "tree": generate_tree_graph,
    "grid": generate_grid_graph,
}


def get_graph(graph_type: str, num_vertices: int, seed: int = 42) -> tuple[list[list[int]], dict[str, Any]]:
    if graph_type not in GENERATORS:
        raise ValueError(f"Unknown graph_type '{graph_type}'. Use one of: {list(GENERATORS)}")
    return GENERATORS[graph_type](num_vertices, seed=seed)


def list_sample_input_files(data_dir: str | None = None) -> list[str]:
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.isdir(data_dir):
        return []
    return sorted(
        os.path.join(data_dir, name)
        for name in os.listdir(data_dir)
        if name.endswith(".json")
    )


def save_sample_graphs(data_dir: str | None = None) -> None:
    """Create JSON files used as manual/file input examples."""
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)

    samples = [
        {
            "filename": "sample_small.json",
            "vertices": 6,
            "graph_type": "manual",
            "edges": [[0, 1], [0, 2], [1, 3], [2, 3], [3, 4], [4, 5]],
        },
        {
            "filename": "sample_disconnected.json",
            "vertices": 8,
            "graph_type": "manual",
            "edges": [[0, 1], [1, 2], [3, 4], [5, 6], [6, 7]],
        },
    ]

    for sample in samples:
        path = os.path.join(data_dir, sample["filename"])
        payload = {
            "vertices": sample["vertices"],
            "directed": False,
            "graph_type": sample["graph_type"],
            "edges": sample["edges"],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
