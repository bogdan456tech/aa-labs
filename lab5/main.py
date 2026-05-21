"""
Lab 5 — Empirical analysis of Prim and Kruskal (MST).
Run: python main.py
"""

import os
import sys
import time

import matplotlib.pyplot as plt

LAB5_DIR = os.path.dirname(os.path.abspath(__file__))
if LAB5_DIR not in sys.path:
    sys.path.insert(0, LAB5_DIR)

from algorithms.kruskal import kruskal
from algorithms.prim import prim
from input_data import edges_from_adjacency, get_graph, save_sample_graph

VERTEX_SIZES = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
GRAPH_TYPES = ["sparse", "dense"]
REPEAT_RUNS = 3


def _time_run(run_fn):
    best = None
    for _ in range(REPEAT_RUNS):
        start = time.perf_counter()
        result = run_fn()
        elapsed = time.perf_counter() - start
        if best is None or elapsed < best[0]:
            best = (elapsed, result)
    return best


def benchmark_graph(adjacency_list):
    n = len(adjacency_list)
    edge_list = edges_from_adjacency(adjacency_list)

    prim_time, (prim_weight, prim_ops) = _time_run(lambda: prim(adjacency_list, 0))
    kruskal_time, (kruskal_weight, kruskal_ops) = _time_run(
        lambda: kruskal(n, edge_list)
    )

    return {
        "prim": {"time": prim_time, "weight": prim_weight, "operations": prim_ops},
        "kruskal": {"time": kruskal_time, "weight": kruskal_weight, "operations": kruskal_ops},
        "mst_match": abs(prim_weight - kruskal_weight) < 1e-6,
    }


def run_benchmarks():
    results = {
        graph_type: {
            "sizes": [],
            "prim_times": [],
            "kruskal_times": [],
            "prim_ops": [],
            "kruskal_ops": [],
        }
        for graph_type in GRAPH_TYPES
    }

    print("\n" + "=" * 125)
    print(" EMPIRICAL ANALYSIS: PRIM vs KRUSKAL (MST) ".center(125, "="))
    print("=" * 125)
    print(
        f"{'Type':<8} | {'V':<6} | {'E':<8} | {'Prim (s)':<12} | {'Kruskal (s)':<12} | "
        f"{'Prim ops':<10} | {'Kruskal ops':<12} | {'MST OK':<6}"
    )
    print("-" * 125)

    for graph_type in GRAPH_TYPES:
        for v in VERTEX_SIZES:
            adjacency_list, meta = get_graph(graph_type, v, seed=42)
            metrics = benchmark_graph(adjacency_list)

            results[graph_type]["sizes"].append(meta["vertices"])
            results[graph_type]["prim_times"].append(metrics["prim"]["time"])
            results[graph_type]["kruskal_times"].append(metrics["kruskal"]["time"])
            results[graph_type]["prim_ops"].append(metrics["prim"]["operations"])
            results[graph_type]["kruskal_ops"].append(metrics["kruskal"]["operations"])

            ok = "yes" if metrics["mst_match"] else "no"
            print(
                f"{graph_type:<8} | {meta['vertices']:<6} | {meta['edges']:<8} | "
                f"{metrics['prim']['time']:<12.6f} | {metrics['kruskal']['time']:<12.6f} | "
                f"{metrics['prim']['operations']:<10} | {metrics['kruskal']['operations']:<12} | {ok:<6}"
            )

    return results


def plot_results(results, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(12, 7))
    for graph_type in GRAPH_TYPES:
        sizes = results[graph_type]["sizes"]
        plt.plot(sizes, results[graph_type]["prim_times"], marker="o", label=f"Prim ({graph_type})")
        plt.plot(
            sizes,
            results[graph_type]["kruskal_times"],
            marker="s",
            linestyle="--",
            label=f"Kruskal ({graph_type})",
        )

    plt.title("Prim vs Kruskal — Execution Time")
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
        ax.plot(sizes, results[graph_type]["prim_times"], marker="o", label="Prim")
        ax.plot(sizes, results[graph_type]["kruskal_times"], marker="s", linestyle="--", label="Kruskal")
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
        plt.plot(sizes, results[graph_type]["prim_ops"], marker="o", label=f"Prim ops ({graph_type})")
        plt.plot(
            sizes,
            results[graph_type]["kruskal_ops"],
            marker="s",
            linestyle="--",
            label=f"Kruskal ops ({graph_type})",
        )

    plt.title("Prim vs Kruskal — Operations Count")
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
    save_sample_graph(os.path.join(LAB5_DIR, "data"))
    results = run_benchmarks()

    for output_dir in [os.path.join(LAB5_DIR, "graphs"), os.path.join(LAB5_DIR, "latex", "graphs")]:
        plot_results(results, output_dir)


if __name__ == "__main__":
    main()
