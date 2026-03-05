import time
import json
import os
import sys
import re
import importlib
import matplotlib.pyplot as plt

# 1. SET HIGH RECURSION LIMIT
# Essential for Lomuto/Hoare on structured data to prevent StackOverflow
sys.setrecursionlimit(10**7)

def run_benchmarks():
    # 2. SETUP PATHS
    base_dir = os.path.dirname(__file__)
    
    # Path to your sorting algorithms folder
    algo_folder = os.path.join(base_dir, "sorting_algorithms")
    
    # Add the folder to sys.path so importlib can find the files
    if algo_folder not in sys.path:
        sys.path.append(algo_folder)

    data_root = os.path.join(base_dir, "data")
    graph_root = os.path.join(base_dir, "graphs")

    # 3. ALGORITHM CONFIGURATION
    # (Module_Name, Function_Name)
    algorithms = {
        "Quick V1 (Lom)": ("quicksort1", "start_quick_sort"),
        "Quick V2 (Hoa)": ("quicksort2", "start_quick_sort_hoare_fixed"),
        "Merge V1 (Bas)": ("mergesort1", "start_merge_sort"),
        "Merge V2 (Ada)": ("mergesort2", "start_merge_sort"),
        "Persian Sort": ("persiansort", "persiansort"),
        "Heap V1 (Rec)": ("heapsort1", "heap_sort"),
        "Heap V2 (Flo)": ("heapsort2", "heap_sort")
    }

    # 4. TASK STRUCTURE (Folder hierarchy)
    task_structure = [
        ("unsorted", ["big_numbers", "small_numbers_big_range_1", "small_numbers_big_range_2"]),
        ("sorted", ["small_range", "big_range"]),
        ("sorted_desc", ["small_range", "big_range"]),
        ("duplicates", ["small_range", "big_range"]),
        ("organ", ["small_range", "big_range"])
    ]

    for category, subfolders in task_structure:
        for sub in subfolders:
            current_path = os.path.join(data_root, category, sub)
            if not os.path.exists(current_path):
                continue

            print(f"\n{'='*145}")
            print(f" TESTING: {category.upper()} / {sub.upper()} ".center(145, "="))
            header = f"{'N Size':<12} | " + " | ".join([f"{label:<15}" for label in algorithms])
            print(header)
            print("-" * len(header))

            # Regex to sort files by the N number in the filename (e.g., data_100.json)
            files = sorted([f for f in os.listdir(current_path) if f.endswith(".json")], 
                           key=lambda x: int(re.search(r'_(\d+)\.json', x).group(1)))
            
            results = {label: {"ns": [], "times": []} for label in algorithms}

            for file_name in files:
                n = int(re.search(r'_(\d+)\.json', file_name).group(1))
                with open(os.path.join(current_path, file_name), 'r') as f:
                    data = json.load(f)

                row = f"{n:<12} | "
                for label, (mod_name, func_name) in algorithms.items():
                    skip = False
                    
                    # --- PERFORMANCE SAFETY RULES ---
                    # 1. Skip Lomuto in specific high-duplicate stress folder
                    if label == "Quick V1 (Lom)":
                        if sub == "small_numbers_big_range_2":
                            skip = True
                        # 2. Skip Lomuto for Big Ranges in non-random sets (prevent O(N^2) hang)
                        elif n > 20000 and not (category == "unsorted" and sub in ["big_numbers", "small_numbers_big_range_1"]):
                            skip = True
                    
                    # 3. Skip Hoare for Organ Big Range (Middle Pivot Trap)
                    if label == "Quick V2 (Hoa)":
                        if category == "organ" and sub == "big_range" and n > 20000:
                            skip = True

                    if skip:
                        row += f"{'SKIPPED':<15} | "
                        continue

                    try:
                        # 5. DYNAMIC IMPORT
                        module = importlib.import_module(mod_name)
                        importlib.reload(module) # Ensure fresh state
                        func = getattr(module, func_name)
                        
                        # Copy data to ensure in-place sorts don't affect next runs
                        data_copy = list(data)
                        
                        start = time.perf_counter()
                        func(data_copy)
                        elapsed = time.perf_counter() - start
                        
                        results[label]["ns"].append(n)
                        results[label]["times"].append(elapsed)
                        row += f"{elapsed:<15.5f} | "
                    except Exception as e:
                        row += f"{'ERROR':<15} | "
                print(row)

            # --- 6. PLOTTING AND SAVING ---
            if any(d["ns"] for d in results.values()):
                plt.figure(figsize=(12, 7))
                for label, d in results.items():
                    if d["ns"]: 
                        plt.plot(d["ns"], d["times"], marker='o', markersize=4, label=label)
                
                plt.title(f"Empirical Analysis: {category.replace('_', ' ').title()} ({sub})", fontweight='bold')
                plt.xlabel("Input Size (N)")
                plt.ylabel("Execution Time (Seconds)")
                plt.legend(loc='upper left', fontsize='small', framealpha=0.9)
                plt.grid(True, linestyle='--', alpha=0.6)
                plt.tight_layout()
                
                # Ensure output directory exists
                out_graph_dir = os.path.join(graph_root, category, sub)
                os.makedirs(out_graph_dir, exist_ok=True)
                
                plt.savefig(os.path.join(out_graph_dir, "analysis.png"), dpi=300)
                plt.close()

if __name__ == "__main__":
    run_benchmarks()