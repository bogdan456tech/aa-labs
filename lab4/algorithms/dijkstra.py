import heapq


def dijkstra(adjacency_list, start=0):
    """
    Single-source shortest paths (non-negative weights).
    adjacency_list[u] = list of (neighbor, weight).
    Returns (distances, operations_count).
    """
    n = len(adjacency_list)
    if n == 0:
        return [], 0

    start = start % n
    distances = [float("inf")] * n
    distances[start] = 0
    operations = 0

    heap = [(0, start)]

    while heap:
        current_dist, node = heapq.heappop(heap)
        if current_dist > distances[node]:
            continue

        for neighbor, weight in adjacency_list[node]:
            operations += 1
            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return distances, operations
