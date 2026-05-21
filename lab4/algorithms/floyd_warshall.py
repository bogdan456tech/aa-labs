def floyd_warshall(weight_matrix):
    """
    All-pairs shortest paths using dynamic programming.
    weight_matrix[i][j] = edge weight, inf if no edge, 0 on diagonal.
    Returns (distance_matrix, operations_count).
    """
    n = len(weight_matrix)
    if n == 0:
        return [], 0

    dist = [row[:] for row in weight_matrix]
    operations = 0

    for k in range(n):
        for i in range(n):
            row_ik = dist[i][k]
            for j in range(n):
                operations += 1
                through_k = row_ik + dist[k][j]
                if through_k < dist[i][j]:
                    dist[i][j] = through_k

    return dist, operations
