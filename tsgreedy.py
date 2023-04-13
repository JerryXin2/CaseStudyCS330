import os
import csv
import math
import matplotlib.pyplot as plt

def read_csv(csv_path, Tid):
    """Returns the list of points with a trajectory id equal to Tid."""
    T = []
    with open(csv_path) as file:
        reader = csv.reader(file, delimiter = ",")

        next(file)
        for row in reader:
            if row[1] == Tid:
                T.append((float(row[2]), float(row[3])))

    return T

def calculate_distance(point, line_segment):
    """Returns the distance between a point and its projection onto a line segment"""
    a, b = line_segment
    x, y = point
    segment_length_squared = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    if segment_length_squared == 0:
        return min(math.dist(point, a), math.dist(point, b))

    t = ((x - a[0]) * (b[0] - a[0]) + (y - a[1]) * (b[1] - a[1])) / segment_length_squared

    if t < 0:
        return math.dist(point, a)
    elif t > 1:
        return math.dist(point, b)

    closest_point = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

    return math.dist(point, closest_point)

def TSGreedy(T, epsilon):
    """Returns the epsilon-simplification of the trajectory T."""
    index = 0
    error = 0
    TSGreedyT = []

    for i in range(1, len(T) - 1):
        distance = calculate_distance(T[i], (T[0], T[-1]))
        if distance > error:
            index = i
            error = distance
    
    # If the error is higher than epsilon then recursively call twice
    if error >= epsilon:
        first_recursion1 = TSGreedy(T[:index+1], epsilon)[:-1]
        first_recursion2 = TSGreedy(T[index:], epsilon)
        TSGreedyT = first_recursion1 + first_recursion2
    else:
        TSGreedyT = [T[0], T[-1]]

    return TSGreedyT

def plot(fig_path, T, TSGreedyT):
    """Generates and saves a visualization of a trajectory T and its simplification TSGreedyT"""
    Tx = []
    Ty = []
    TSGreedyTx = []
    TSGreedyTy = []

    for _, tuple in enumerate(T):
        Tx.append(tuple[0])
        Ty.append(tuple[1])
    
    for _, tuple in enumerate(TSGreedyT):
        TSGreedyTx.append(tuple[0])
        TSGreedyTy.append(tuple[1])

    fig, ax = plt.subplots()
    ax.plot(Tx, Ty, label = "Trajectory")
    ax.plot(TSGreedyTx, TSGreedyTy, "--", label = "Simplification")
    ax.legend()

    fig.savefig(fig_path, dpi = 500)

if __name__ == "__main__":
    """Runs the list of experiments designated in the case study description"""
    csv_path = "./data/geolife-cars.csv"

    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    if not os.path.exists("./figures/task_2"):
        os.mkdir("./figures/task_2")

    # Naming convention: "./figures/task_2/Tid_epsilon.png"
    for e in [0.03, 0.1, 0.3]:
        T = read_csv(csv_path, "128-20080503104400")
        TSGreedyT = TSGreedy(T, e)
        plot(f"./figures/task_2/128-20080503104400_{e}.png", T, TSGreedyT)

    for Tid in ["128-20080503104400", "010-20081016113953", "115-20080520225850", "115-20080615225707"]:
        T = read_csv(csv_path, Tid)
        TSGreedyT = TSGreedy(T, 0.03)
        plot(f"./figures/task_2/{Tid}_0.03.png", T, TSGreedyT)
        print(f"Compression Ratio of T = {Tid}: {len(T)/len(TSGreedyT)}")
