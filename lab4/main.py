"""
Lab 4 — Empirical analysis of Dijkstra and Floyd-Warshall.
Run: python main.py
"""

import os
import sys
import time

import matplotlib.pyplot as plt

LAB4_DIR = os.path.dirname(os.path.abspath(__file__))
if LAB4_DIR not in sys.path:
    sys.path.insert(0, LAB4_DIR)

from algorithms.dijkstra import dijkstra
from algorithms.floyd_warshall import floyd_warshall
from input_data import adjacency_list_to_matrix, get_graph, save_sample_graph

VERTEX_SIZES = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
GRAPH_TYPES = ["sparse", "dense"]
REPEAT_RUNS = 3
START_NODE = 0


def _time_run(run_fn):
    best = None
    for _ in range(REPEAT_RUNS):
        start = time.perf_counter()
        result = run_fn()
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best[0]:
            best = (elapsed, result)
    return best


def benchmark_graph(adjacency_list, start_node=START_NODE):
    matrix = adjacency_list_to_matrix(adjacency_list)

    dijk_time, (_, dijk_ops) = _time_run(lambda: dijkstra(adjacency_list, start_node))
    floyd_time, (_, floyd_ops) = _time_run(lambda: floyd_warshall(matrix))

    return {
        "dijkstra": {"time": dijk_time, "operations": dijk_ops},
        "floyd": {"time": floyd_time, "operations": floyd_ops},
    }


def run_benchmarks():
    results = {
        graph_type: {
            "sizes": [],
            "dijk_times": [],
            "floyd_times": [],
            "dijk_ops": [],
            "floyd_ops": [],
        }
        for graph_type in GRAPH_TYPES
    }

    print("\n" + "=" * 120)
    print(" EMPIRICAL ANALYSIS: DIJKSTRA vs FLOYD-WARSHALL ".center(120, "="))
    print("=" * 120)
    print(
        f"{'Type':<8} | {'V':<6} | {'E':<8} | {'Dijkstra (s)':<14} | "
        f"{'Floyd (s)':<14} | {'Dijk ops':<12} | {'Floyd ops':<12}"
    )
    print("-" * 120)

    for graph_type in GRAPH_TYPES:
        for v in VERTEX_SIZES:
            adjacency_list, meta = get_graph(graph_type, v, seed=42)
            metrics = benchmark_graph(adjacency_list, START_NODE)

            results[graph_type]["sizes"].append(meta["vertices"])
            results[graph_type]["dijk_times"].append(metrics["dijkstra"]["time"])
            results[graph_type]["floyd_times"].append(metrics["floyd"]["time"])
            results[graph_type]["dijk_ops"].append(metrics["dijkstra"]["operations"])
            results[graph_type]["floyd_ops"].append(metrics["floyd"]["operations"])

            print(
                f"{graph_type:<8} | {meta['vertices']:<6} | {meta['edges']:<8} | "
                f"{metrics['dijkstra']['time']:<14.6f} | {metrics['floyd']['time']:<14.6f} | "
                f"{metrics['dijkstra']['operations']:<12} | {metrics['floyd']['operations']:<12}"
            )

    return results


def plot_results(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(12, 7))
    for graph_type in GRAPH_TYPES:
        sizes = results[graph_type]["sizes"]
        plt.plot(sizes, results[graph_type]["dijk_times"], marker="o", label=f"Dijkstra ({graph_type})")
        plt.plot(
            sizes,
            results[graph_type]["floyd_times"],
            marker="s",
            linestyle="--",
            label=f"Floyd-Warshall ({graph_type})",
        )

    plt.title("Dijkstra vs Floyd-Warshall — Execution Time")
    plt.xlabel("Number of vertices (V)")
    plt.ylabel("Time (seconds)")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9, ncol=2)
    plt.tight_layout()
    path1 = os.path.join(output_dir, "time_comparison.png")
    plt.savefig(path1, dpi=150)
    plt.close()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, graph_type in zip(axes, GRAPH_TYPES):
        sizes = results[graph_type]["sizes"]
        ax.plot(sizes, results[graph_type]["dijk_times"], marker="o", label="Dijkstra")
        ax.plot(sizes, results[graph_type]["floyd_times"], marker="s", linestyle="--", label="Floyd-Warshall")
        ax.set_title(f"Graph type: {graph_type}")
        ax.set_xlabel("V")
        ax.set_ylabel("Time (s)")
        ax.grid(True, alpha=0.3)
        ax.legend()

    fig.suptitle("Execution Time by Graph Density", fontsize=14)
    fig.tight_layout()
    path2 = os.path.join(output_dir, "time_by_graph_type.png")
    fig.savefig(path2, dpi=150)
    plt.close()

    plt.figure(figsize=(12, 7))
    for graph_type in GRAPH_TYPES:
        sizes = results[graph_type]["sizes"]
        plt.plot(sizes, results[graph_type]["dijk_ops"], marker="o", label=f"Dijkstra ops ({graph_type})")
        plt.plot(
            sizes,
            results[graph_type]["floyd_ops"],
            marker="s",
            linestyle="--",
            label=f"Floyd ops ({graph_type})",
        )

    plt.title("Dijkstra vs Floyd-Warshall — Operations Count")
    plt.xlabel("Number of vertices (V)")
    plt.ylabel("Operations")
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=9, ncol=2)
    plt.tight_layout()
    path3 = os.path.join(output_dir, "operations_comparison.png")
    plt.savefig(path3, dpi=150)
    plt.close()

    print("\nSaved plots:")
    print(f"  - {path1}")
    print(f"  - {path2}")
    print(f"  - {path3}")


def main():
    save_sample_graph(os.path.join(LAB4_DIR, "data"))
    results = run_benchmarks()

    graphs_dir = os.path.join(LAB4_DIR, "graphs")
    latex_graphs_dir = os.path.join(LAB4_DIR, "latex", "graphs")
    plot_results(results, graphs_dir)
    plot_results(results, latex_graphs_dir)


if __name__ == "__main__":
    main()
