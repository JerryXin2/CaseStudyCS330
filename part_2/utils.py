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

    return (dtws[n - 1][m - 1] / sizes[n - 1][m - 1])**0.5


def calculate_distance(point, segment):
    a, b = segment
    segment_length_squared = distance2(a, b)

    if segment_length_squared == 0:
        return min(distance(point, a), distance(point, b))

    t = ((point[0] - a[0]) * (b[0] - a[0]) + (point[1] - a[1]) * (b[1] - a[1])) / segment_length_squared

    if t < 0:
        return distance(point, a)
    elif t > 1:
        return distance(point, b)

    closest_point = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

    return distance(point, closest_point)


def ts_greedy(trajectory, epsilon):
    if epsilon == 0:
        return trajectory

    ret = []
    index = 0
    error = 0
    for i in range(1, len(trajectory) - 1):
        distance = calculate_distance(trajectory[i], (trajectory[0], trajectory[-1]))
        if distance > error:
            index = i
            error = distance

    if error >= epsilon:
        recursion_1 = ts_greedy(trajectory[:index+1], epsilon)[:-1]
        recursion_2 = ts_greedy(trajectory[index:], epsilon)
        ret = recursion_1 + recursion_2
    else:
        ret = [trajectory[0], trajectory[-1]]

    return ret


def read_csv(csv_path, tids=None):
    trajectories = {}

    with open(csv_path) as file:
        reader = csv.reader(file, delimiter=",")

        next(file)
        for row in reader:
            tid = row[0]

            if tids is None:
                if tid not in trajectories:
                    trajectories[tid] = []
                trajectories[tid].append((float(row[1]), float(row[2])))
            else:
                if tid in tids:
                    if tid not in trajectories:
                        trajectories[tid] = []
                    trajectories[tid].append((float(row[1]), float(row[2])))

    return trajectories