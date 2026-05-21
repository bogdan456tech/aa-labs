from collections import deque


def bfs(adjacency_list, start=0):
    """
    Breadth-first search on an adjacency list.
    Returns (visit_order, visited_count, operations_count).
    operations_count counts neighbor checks (useful for empirical comparison).
    """
    n = len(adjacency_list)
    if n == 0:
        return [], 0, 0

    start = start % n
    visited = [False] * n
    order = []
    operations = 0

    queue = deque([start])
    visited[start] = True

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in adjacency_list[node]:
            operations += 1
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return order, sum(visited), operations
