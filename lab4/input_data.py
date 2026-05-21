"""
Weighted graph generators for Lab 4 (sparse / dense).
"""

import json
import math
import os
import random
from typing import Any


INF = float("inf")


def build_adjacency_list(num_vertices: int, edges: list[list], directed: bool = False) -> list[list[tuple[int, float]]]:
    adj = [[] for _ in range(num_vertices)]
    for edge in edges:
        u, v = int(edge[0]), int(edge[1])
        w = float(edge[2]) if len(edge) > 2 else 1.0
        if u == v:
            continue
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))

    for neighbors in adj:
        neighbors.sort(key=lambda item: item[0])
    return adj


def adjacency_list_to_matrix(adjacency_list: list[list[tuple[int, float]]]) -> list[list[float]]:
    n = len(adjacency_list)
    matrix = [[INF] * n for _ in range(n)]
    for i in range(n):
        matrix[i][i] = 0.0
        for j, w in adjacency_list[i]:
            if w < matrix[i][j]:
                matrix[i][j] = w
    return matrix


def _random_weighted_edges(num_vertices: int, num_edges: int, rng: random.Random) -> list[list]:
    edge_set: set[tuple[int, int]] = set()
    edges: list[list] = []
    max_attempts = num_edges * 25
    attempts = 0

    while len(edges) < num_edges and attempts < max_attempts:
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
        weight = rng.randint(1, 100)
        edges.append([u, v, weight])
        attempts += 1

    return edges


def generate_sparse_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[tuple[int, float]]], dict[str, Any]]:
    rng = random.Random(seed)
    num_edges = max(num_vertices - 1, num_vertices)
    edges = _random_weighted_edges(num_vertices, num_edges, rng)
    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "sparse",
        "directed": False,
        "seed": seed,
    }
    return build_adjacency_list(num_vertices, edges), meta


def generate_dense_graph(num_vertices: int, seed: int = 42) -> tuple[list[list[tuple[int, float]]], dict[str, Any]]:
    rng = random.Random(seed)
    num_edges = min(
        num_vertices * (num_vertices - 1) // 2,
        int(num_vertices * max(2, math.log2(max(num_vertices, 2)))),
    )
    edges = _random_weighted_edges(num_vertices, num_edges, rng)
    meta = {
        "vertices": num_vertices,
        "edges": len(edges),
        "graph_type": "dense",
        "directed": False,
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
        "directed": False,
        "graph_type": "manual",
        "edges": [[0, 1, 4], [0, 2, 1], [1, 2, 2], [1, 3, 5], [2, 3, 8], [3, 4, 2], [2, 4, 10]],
    }
    path = os.path.join(data_dir, "sample_weighted.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=2)
