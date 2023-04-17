import csv

def distance2(p, q):
    return (p[0] - q[0])**2 + (p[1] - q[1])**2

def distance(p, q):
    return distance2(p, q)**0.5

def dtw_distance(P, Q):
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

    return dtws[n - 1][m - 1]

def read_csv(csv_path, tids):
    trajectories = {}

    with open(csv_path) as file:
        reader = csv.reader(file, delimiter=",")

        next(file)
        for row in reader:
            tid = row[0]
            if tid in tids:
                if tid not in trajectories:
                    trajectories[tid] = []
                trajectories[tid].append((row[1], row[2]))

    return trajectories