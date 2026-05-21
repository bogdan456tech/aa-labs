def dfs(adjacency_list, start=0):
    """
    Depth-first search (iterative, stack-based) on an adjacency list.
    Returns (visit_order, visited_count, operations_count).
    """
    n = len(adjacency_list)
    if n == 0:
        return [], 0, 0

    start = start % n
    visited = [False] * n
    order = []
    operations = 0

    stack = [start]
    visited[start] = True

    while stack:
        node = stack.pop()
        order.append(node)

        # Reverse so smaller-index neighbors are visited first (stable DFS order).
        for neighbor in reversed(adjacency_list[node]):
            operations += 1
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)

    return order, sum(visited), operations
