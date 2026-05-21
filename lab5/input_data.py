"""
Connected weighted graph generators for Lab 5 (MST: Prim & Kruskal).
"""

import json
import math
import os
import random
from typing import Any


def build_adjacency_list(num_vertices: int, edges: list[list]) -> list[list[tuple[int, float]]]:
    adj = [[] for _ in range(num_vertices)]
    for edge in edges:
        u, v = int(edge[0]), int(edge[1])
        w = float(edge[2]) if len(edge) > 2 else 1.0
        if u == v:
            continue
        adj[u].append((v, w))
        adj[v].append((u, w))

    for neighbors in adj:
        neighbors.sort(key=lambda item: item[0])
    return adj


def edges_from_adjacency(adjacency_list: list[list[tuple[int, float]]]) -> list[tuple[float, int, int]]:
    edge_set: set[tuple[int, int, float]] = set()
    edges: list[tuple[float, int, int]] = []
    for u, neighbors in enumerate(adjacency_list):
        for v, w in neighbors:
            if u < v:
                key = (u, v, w)
                if key not in edge_set:
                    edge_set.add(key)
                    edges.append((w, u, v))
    return edges


def _connected_edges(num_vertices: int, num_edges: int, rng: random.Random) -> list[list]:
    """Build a connected undirected graph with at least num_vertices-1 edges."""
    max_edges = num_vertices * (num_vertices - 1) // 2
    num_edges = min(max_edges, max(num_vertices - 1, num_edges))

    edge_set: set[tuple[int, int]] = set()
    edges: list[list] = []

    # Random spanning tree guarantees connectivity
    for v in range(1, num_vertices):
        u = rng.randrange(v)
        w = rng.randint(1, 100)
        key = (min(u, v), max(u, v))
        edge_set.add(key)
        edges.append([u, v, w])

    attempts = 0
    while len(edges) < num_edges and attempts < num_edges * 25:
        u = rng.randrange(num_vertices)
        v = rng.randrange(num_vertices)
        if u == v:
            attempts += 1
            continue
        key = (min(u, v), max(u, v))
        if key in edge_set:
            attempts += 1
            continue
        edge_set.add(key)
        edges.append([u, v, rng.randint(1, 100)])
        attempts += 1

    return edges


def generate_sparse_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[tuple[int, float]]], dict[str, Any]]:
    """Sparse connected graph: E = V - 1 (tree)."""
    rng = random.Random(seed)
    edges = _connected_edges(num_vertices, num_vertices - 1, rng)
    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "sparse",
        "connected": True,
        "seed": seed,
    }
    return build_adjacency_list(num_vertices, edges), meta


def generate_dense_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[tuple[int, float]]], dict[str, Any]]:
    """Dense connected graph: E ~= V * log2(V)."""
    rng = random.Random(seed)
    num_edges = min(
        num_vertices * (num_vertices - 1) // 2,
        int(num_vertices * max(2, math.log2(max(num_vertices, 2)))),
    )
    edges = _connected_edges(num_vertices, num_edges, rng)
    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "dense",
        "connected": True,
        "seed": seed,
    }
    return build_adjacency_list(num_vertices, edges), meta


GENERATORS = {
    "sparse": generate_sparse_graph,
    "dense": generate_dense_graph,
}


def get_graph(graph_type: str, num_vertices: int, seed: int = 42):
    if graph_type not in GENERATORS:
        raise ValueError(f"Unknown graph_type '{graph_type}'. Use: {list(GENERATORS)}")
    return GENERATORS[graph_type](num_vertices, seed=seed)


def save_sample_graph(data_dir: str | None = None) -> None:
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "data")
    os.makedirs(data_dir, exist_ok=True)
    sample = {
        "vertices": 5,
        "graph_type": "manual",
        "edges": [[0, 1, 2], [0, 3, 6], [1, 2, 3], [1, 4, 5], [2, 4, 7], [3, 4, 9]],
    }
    with open(os.path.join(data_dir, "sample_mst.json"), "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=2)
