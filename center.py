

def distance2(p, q):
    """Returns the square of the Euclidean distance between p and q."""
    return (p[0] - q[0])**2 + (p[1] - q[1])**2

def dtw_distance(P, Q):
    """Returns the dynamic time warping of P and Q"""
    n, m = len(P), len(Q)

    distances, sizes, dtws = [[0 for i in range(m)] for j in range(n)], [[0 for i in range(m)] for j in range(n)], [[0 for i in range(m)] for j in range(n)]

    for i in range(n):
        for j in range(m):
            distances[i][j] = distance2(P[i], Q[j])

    sizes[0][0] = 1
    dtws[0][0] = distances[0][0]

    for i in range(1, n):
        sizes[i][0] = sizes[i - 1][0] + 1
        dtws[i][0] = (distances[i][0] + sizes[i - 1][0] * dtws[i - 1][0]) / (sizes[i - 1][0] + 1)

    for j in range(1, m):
        sizes[0][j] = sizes[0][j - 1] + 1
        dtws[0][j] = (distances[0][j] + sizes[0][j - 1] * dtws[0][j - 1]) / (sizes[0][j - 1] + 1)

    for i in range(1, n):
        for j in range(1, m):
            candidates = [(distances[i][j] + sizes[i - 1][j] * dtws[i - 1][j]) / (sizes[i - 1][j] + 1),
                          (distances[i][j] + sizes[i][j - 1] * dtws[i][j - 1]) / (sizes[i][j - 1] + 1),
                          (distances[i][j] + sizes[i - 1][j - 1] * dtws[i - 1][j - 1]) / (sizes[i - 1][j - 1] + 1)]
            if candidates[0] == min(candidates):
                sizes[i][j] = sizes[i - 1][j] + 1
            elif candidates[1] == min(candidates):
                sizes[i][j] = sizes[i][j - 1] + 1
            else:
                sizes[i][j] = sizes[i - 1][j - 1] + 1
            dtws[i][j] = min(candidates)

    # Traces the optimal path in reverse to find the edges
    path = []
    i, j = n - 1, m - 1
    while i > 0 or j > 0:
        path.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            candidates = [(distances[i][j] + sizes[i - 1][j] * dtws[i - 1][j]) / (sizes[i - 1][j] + 1),
                          (distances[i][j] + sizes[i][j - 1] * dtws[i][j - 1]) / (sizes[i][j - 1] + 1),
                          (distances[i][j] + sizes[i - 1][j - 1] * dtws[i - 1][j - 1]) / (sizes[i - 1][j - 1] + 1)]
            if candidates[0] == min(candidates):
                i -= 1
            elif candidates[1] == min(candidates):
                j -= 1
            else:
                i -= 1
                j -= 1
    path.append((0, 0))

    return dtws[n - 1][m - 1]
