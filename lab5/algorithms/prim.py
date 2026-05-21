import heapq


def prim(adjacency_list, start=0):
    """
    Prim MST with min-heap (adjacency list of (neighbor, weight)).
    Returns (mst_total_weight, operations_count).
    """
    n = len(adjacency_list)
    if n == 0:
        return 0.0, 0

    start = start % n
    in_mst = [False] * n
    key = [float("inf")] * n
    key[start] = 0
    operations = 0

    heap = [(0.0, start)]

    while heap:
        weight, node = heapq.heappop(heap)
        if in_mst[node]:
            continue
        in_mst[node] = True

        for neighbor, edge_weight in adjacency_list[node]:
            operations += 1
            if not in_mst[neighbor] and edge_weight < key[neighbor]:
                key[neighbor] = edge_weight
                heapq.heappush(heap, (edge_weight, neighbor))

    return sum(key), operations
