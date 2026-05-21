"""
Lab 3 — Empirical analysis of BFS and DFS.

Metrics:
  - execution time (seconds)
  - visited nodes
  - neighbor checks (operations)

Run:
  python main.py
"""

import os
import sys
import time

import matplotlib.pyplot as plt

# Allow imports from lab3 folder when executed as script.
LAB3_DIR = os.path.dirname(os.path.abspath(__file__))
if LAB3_DIR not in sys.path:
    sys.path.insert(0, LAB3_DIR)

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from input_data import (
    GENERATORS,
    get_graph,
    list_sample_input_files,
    load_graph_from_json,
    save_sample_graphs,
)


# Input sizes for empirical analysis (number of vertices V).
VERTEX_SIZES = [100, 250, 500, 750, 1000, 1500, 2000, 3000]

# Graph families to compare.
GRAPH_TYPES = ["sparse", "dense", "tree", "grid"]

# Repeat each measurement and keep the minimum (reduces timer noise).
REPEAT_RUNS = 3
START_NODE = 0


def _time_algorithm(run_fn):
    best = None
    for _ in range(REPEAT_RUNS):
        start = time.perf_counter()
        order, visited, operations = run_fn()
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best[0]:
            best = (elapsed, order, visited, operations)
    return best


def benchmark_graph(adjacency_list, start_node=START_NODE):
    bfs_time, bfs_order, bfs_visited, bfs_ops = _time_algorithm(
        lambda: bfs(adjacency_list, start_node)
    )
    dfs_time, dfs_order, dfs_visited, dfs_ops = _time_algorithm(
        lambda: dfs(adjacency_list, start_node)
    )

    return {
        "bfs": {"time": bfs_time, "visited": bfs_visited, "operations": bfs_ops, "order_len": len(bfs_order)},
        "dfs": {"time": dfs_time, "visited": dfs_visited, "operations": dfs_ops, "order_len": len(dfs_order)},
    }


def run_generated_benchmarks():
    results = {graph_type: {"sizes": [], "bfs_times": [], "dfs_times": [], "bfs_ops": [], "dfs_ops": []} for graph_type in GRAPH_TYPES}

    print("\n" + "=" * 120)
    print(" EMPIRICAL ANALYSIS: GENERATED GRAPHS ".center(120, "="))
    print("=" * 120)
    print(f"{'Type':<8} | {'V':<8} | {'E':<8} | {'BFS (s)':<12} | {'DFS (s)':<12} | {'BFS ops':<10} | {'DFS ops':<10}")
    print("-" * 120)

    for graph_type in GRAPH_TYPES:
        for v in VERTEX_SIZES:
            adjacency_list, meta = get_graph(graph_type, v, seed=42)
            metrics = benchmark_graph(adjacency_list, START_NODE)

            results[graph_type]["sizes"].append(meta["vertices"])
            results[graph_type]["bfs_times"].append(metrics["bfs"]["time"])
            results[graph_type]["dfs_times"].append(metrics["dfs"]["time"])
            results[graph_type]["bfs_ops"].append(metrics["bfs"]["operations"])
            results[graph_type]["dfs_ops"].append(metrics["dfs"]["operations"])

            print(
                f"{graph_type:<8} | {meta['vertices']:<8} | {meta['edges']:<8} | "
                f"{metrics['bfs']['time']:<12.6f} | {metrics['dfs']['time']:<12.6f} | "
                f"{metrics['bfs']['operations']:<10} | {metrics['dfs']['operations']:<10}"
            )

    return results


def run_file_inputs():
    files = list_sample_input_files()
    if not files:
        return

    print("\n" + "=" * 120)
    print(" EMPIRICAL ANALYSIS: JSON FILE INPUT ".center(120, "="))
    print("=" * 120)
    print(f"{'File':<28} | {'V':<4} | {'E':<4} | {'BFS (s)':<12} | {'DFS (s)':<12} | {'BFS visited':<12} | {'DFS visited':<12}")
    print("-" * 120)

    for path in files:
        adjacency_list, meta = load_graph_from_json(path)
        metrics = benchmark_graph(adjacency_list, START_NODE)
        file_name = os.path.basename(path)

        print(
            f"{file_name:<28} | {meta['vertices']:<4} | {meta['edges']:<4} | "
            f"{metrics['bfs']['time']:<12.8f} | {metrics['dfs']['time']:<12.8f} | "
            f"{metrics['bfs']['visited']:<12} | {metrics['dfs']['visited']:<12}"
        )

        # Show traversal orders for small manual graphs (useful for report screenshots).
        if meta["vertices"] <= 20:
            bfs_order, _, _ = bfs(adjacency_list, START_NODE)
            dfs_order, _, _ = dfs(adjacency_list, START_NODE)
            print(f"  BFS order from node {START_NODE}: {bfs_order}")
            print(f"  DFS order from node {START_NODE}: {dfs_order}")


def plot_results(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # 1) Execution time vs number of vertices.
    plt.figure(figsize=(12, 7))
    for graph_type in GRAPH_TYPES:
        sizes = results[graph_type]["sizes"]
        plt.plot(sizes, results[graph_type]["bfs_times"], marker="o", label=f"BFS ({graph_type})")
        plt.plot(sizes, results[graph_type]["dfs_times"], marker="s", linestyle="--", label=f"DFS ({graph_type})")

    plt.title("BFS vs DFS — Execution Time")
    plt.xlabel("Number of vertices (V)")
    plt.ylabel("Time (seconds)")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    time_plot_path = os.path.join(output_dir, "time_comparison.png")
    plt.savefig(time_plot_path, dpi=150)
    plt.show()

    # 2) Separate subplot per graph family (clearer for report screenshots).
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    axes = axes.flatten()

    for ax, graph_type in zip(axes, GRAPH_TYPES):
        sizes = results[graph_type]["sizes"]
        ax.plot(sizes, results[graph_type]["bfs_times"], marker="o", label="BFS")
        ax.plot(sizes, results[graph_type]["dfs_times"], marker="s", linestyle="--", label="DFS")
        ax.set_title(f"Graph type: {graph_type}")
        ax.set_xlabel("V")
        ax.set_ylabel("Time (s)")
        ax.grid(True, alpha=0.3)
        ax.legend()

    fig.suptitle("BFS vs DFS by Input Graph Family", fontsize=14)
    fig.tight_layout()
    family_plot_path = os.path.join(output_dir, "time_by_graph_type.png")
    fig.savefig(family_plot_path, dpi=150)
    plt.show()

    # 3) Operations count comparison.
    plt.figure(figsize=(12, 7))
    for graph_type in GRAPH_TYPES:
        sizes = results[graph_type]["sizes"]
        plt.plot(sizes, results[graph_type]["bfs_ops"], marker="o", label=f"BFS ops ({graph_type})")
        plt.plot(sizes, results[graph_type]["dfs_ops"], marker="s", linestyle="--", label=f"DFS ops ({graph_type})")

    plt.title("BFS vs DFS — Neighbor Checks (Operations)")
    plt.xlabel("Number of vertices (V)")
    plt.ylabel("Operations count")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=8, ncol=2)
    plt.tight_layout()
    ops_plot_path = os.path.join(output_dir, "operations_comparison.png")
    plt.savefig(ops_plot_path, dpi=150)
    plt.show()

    print("\nSaved plots:")
    print(f"  - {time_plot_path}")
    print(f"  - {family_plot_path}")
    print(f"  - {ops_plot_path}")


def print_input_properties():
    print("\nINPUT DATA PROPERTIES USED IN THIS LAB")
    print("-" * 60)
    print("Representation: adjacency list")
    print("Start node: 0")
    print(f"Vertex sizes (V): {VERTEX_SIZES}")
    print(f"Graph families: {list(GENERATORS.keys())}")
    print("  - sparse:  E ~= V")
    print("  - dense:   E ~= V * log2(V)")
    print("  - tree:    E = V - 1")
    print("  - grid:    lattice graph (~4 neighbors per internal node)")
    print("Additional input: JSON files in lab3/data/")
    print("Metrics: execution time, visited nodes, neighbor checks")


def main():
    print_input_properties()

    data_dir = os.path.join(LAB3_DIR, "data")
    save_sample_graphs(data_dir)

    results = run_generated_benchmarks()
    run_file_inputs()

    graphs_dir = os.path.join(LAB3_DIR, "graphs")
    plot_results(results, graphs_dir)


if __name__ == "__main__":
    main()
