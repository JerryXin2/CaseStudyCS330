import os
import csv
import matplotlib.pyplot as plt
from tsgreedy import TSGreedy

def read_csv(csv_path, Pid, Qid):
    """Returns two lists of points with a trajectory id equal to Pid and Qid."""
    P = []
    Q = []

    with open(csv_path) as file:
        reader = csv.reader(file, delimiter = ",")

        next(file)
        for row in reader:
            if row[1] == Pid:
                P.append((float(row[2]), float(row[3])))
            elif row[1] == Qid:
                Q.append((float(row[2]), float(row[3])))
    
    return P, Q

def distance(p, q):
    """Returns the Euclidean distance between p and q."""
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

def distance2(p, q):
    """Returns the square of the Euclidean distance between p and q."""
    return (p[0] - q[0])**2 + (p[1] - q[1])**2

def get_dtw(P, Q):
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

    return dtws[n - 1][m - 1], path

def get_fretchet(P, Q):
    """Returns the Fretchet distance of P and Q"""
    n, m = len(P), len(Q)

    fretchets = [[-1 for i in range(m)] for j in range(n)]
    fretchets[0][0] = distance(P[0], Q[0])

    for i in range(1, n):
        fretchets[i][0] = max(fretchets[i - 1][0], distance(P[i], Q[0]))

    for j in range(1, m):
        fretchets[0][j] = max(fretchets[0][j - 1], distance(P[0], Q[j]))
    
    for i in range(1, n):
        for j in range(1, m):
            fretchets[i][j] = max(min(fretchets[i - 1][j], fretchets[i][j - 1], fretchets[i - 1][j - 1]), distance(P[i], Q[j]))
    
    # Traces the optimal path in reverse to find all the edges
    path = []
    i, j = n-1, m-1
    while i > 0 or j > 0:
        path.append((i, j))
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        else:
            if fretchets[i-1][j] == min(fretchets[i-1][j-1], fretchets[i][j-1], fretchets[i-1][j]):
                i -= 1
            elif fretchets[i][j-1] == min(fretchets[i-1][j-1], fretchets[i][j-1], fretchets[i-1][j]):
                j -= 1
            else:
                i -= 1
                j -= 1
    path.append((0, 0))
    
    return fretchets[n - 1][m - 1], path

def plot(fig_path, P, Q, path):
    """Generates and saves a histogram of the edge lengths in path"""
    lengths = []
    for i, j in path:
        lengths.append(distance(P[i], Q[j]))
    
    fig, ax = plt.subplots()
    ax.hist(lengths, bins = 30)
    ax.set_xlabel("Edge Lengths")
    ax.set_ylabel("Frequency")

    fig.savefig(fig_path, dpi = 500)

if __name__ == "__main__":
    """Runs the list of experiments designated in the case study description"""
    Pids = ["128-20080503104400", "010-20081016113953", "115-20080520225850"]
    Qids = ["128-20080509135846", "010-20080923124453", "115-20080615225707"]

    csv_path = "./data/geolife-cars.csv"

    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    if not os.path.exists("./figures/task_3"):
        os.mkdir("./figures/task_3")

    # Naming convention: "./figures/task_3/metric_Pid_Qid_epsilon.png"
    for i in range(len(Pids)):
        P, Q = read_csv(csv_path, Pids[i], Qids[i])
        dtw, path = get_dtw(P, Q)
        plot(f"./figures/task_3/dtw_{Pids[i]}_{Qids[i]}_0.png", P, Q, path)

        fretchet, path = get_fretchet(P, Q)
        plot(f"./figures/task_3/fretchet_{Pids[i]}_{Qids[i]}_0.png", P, Q, path)

        print(f"DTW for P = {Pids[i]}, Q = {Qids[i]}: {dtw}")
        print(f"Fretchet for P = {Pids[i]}, Q = {Qids[i]}: {fretchet}")

    for e in [0.03, 0.1, 0.3]:
        P, Q = read_csv(csv_path, Pids[2], Qids[2])
        TSGreedyP = TSGreedy(P, e)
        TSGreedyQ = TSGreedy(Q, e)

        dtw, path = get_dtw(TSGreedyP, TSGreedyQ)
        plot(f"./figures/task_3/dtw_{Pids[2]}_{Qids[2]}_{e}.png", TSGreedyP, TSGreedyQ, path)
        print(f"DTW for P = {Pids[2]}, Q = {Qids[2]}, epsilon = {e}: {dtw}")