def kruskal(num_vertices, edges):
    """
    Kruskal MST on undirected weighted edges.
    edges: list of (weight, u, v)
    Returns (mst_total_weight, operations_count).
    """
    parent = list(range(num_vertices))
    rank = [0] * num_vertices
    operations = 0

    def find(x):
        nonlocal operations
        while parent[x] != x:
            operations += 1
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        nonlocal operations
        if rank[a] < rank[b]:
            parent[a] = b
        elif rank[a] > rank[b]:
            parent[b] = a
        else:
            parent[b] = a
            rank[a] += 1
        operations += 1

    sorted_edges = sorted(edges, key=lambda item: item[0])
    mst_weight = 0.0
    edges_used = 0

    for weight, u, v in sorted_edges:
        operations += 1
        root_u = find(u)
        root_v = find(v)
        if root_u != root_v:
            union(root_u, root_v)
            mst_weight += weight
            edges_used += 1
            if edges_used == num_vertices - 1:
                break

    return mst_weight, operations
