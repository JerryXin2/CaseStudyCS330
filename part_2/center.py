import os
import math
import matplotlib.pyplot as plt

from utils import distance, dtw_distance, interpolate, read_csv, ts_greedy


def approach_1(trajectories):
    dtw_dists = {}

    for tid, trajectory in trajectories.items():
        dtw_dists[tid] = 0

        for tid2, trajectory2 in trajectories.items():
            if tid != tid2:
                dtw_dists[tid] += dtw_distance(trajectory, trajectory2)
    
    min_dist = float("inf")
    min_tid = None
    for tid, dist in dtw_dists.items():
        if dist < min_dist:
            min_dist = dist
            min_tid = tid
    
    return trajectories[min_tid]


def approach_2_time(trajectories):
    max_len = 0
    for trajectory in trajectories.values():
        if len(trajectory) > max_len:
            max_len = len(trajectory)
    
    center = []
    for trajectory in trajectories.values():
        values = time_interpolate(trajectory, len(trajectory), max_len)

        if not center:
            center = values
        else:
            center = [(center[i][0] + values[i][0], center[i][1] + values[i][1]) for i in range(len(center))]
            
    return [(c[0]/len(trajectories.items()), c[1]/len(trajectories.items())) for c in center]


def time_interpolate(trajectory, len, max_len):
    values = []

    t = 0
    while t < len - 1:
        t_floor = math.floor(t)
        t_ceil = math.ceil(t)

        values.append(interpolate(trajectory[t_floor], trajectory[t_ceil], t - t_floor))

        t += (len - 1)/(max_len - 1)

    values.append(trajectory[-1])

    return values


def approach_2_dist(trajectories):
    distances = {}
    for tid, trajectory in trajectories.items():
        dist = 0
        for i in range(1, len(trajectory)):
            dist += distance(trajectory[i-1], trajectory[i])
        distances[tid] = dist

    max_dist = 0
    for tid in trajectories.keys():
        if distances[tid] > max_dist:
            max_dist = distances[tid]

    center = []
    for tid, trajectory in trajectories.items():
        values = dist_interpolate(trajectory, distances[tid], max_dist)

        if not center:
            center = values
        else:
            center = [(center[i][0] + values[i][0], center[i][1] + values[i][1]) for i in range(len(center))]
            
    return [(c[0]/len(trajectories.items()), c[1]/len(trajectories.items())) for c in center]


def dist_interpolate(trajectory, dist, max_dist):
    increment = 0.5

    values = []

    d = 0
    last_index = 0
    while d < dist:
        temp = d


        d += increment * dist/max_dist

    

    return values


def average_dtw(center, trajectories):
    total_dtw = 0
    for trajectory in trajectories.values():
        total_dtw += dtw_distance(center, trajectory)
    return total_dtw/len(trajectories.items())


def plot(fig_path, trajectories):
    fig, ax = plt.subplots()

    for label, trajectory in trajectories.items():
        x = [t[0] for t in trajectory]
        y = [t[1] for t in trajectory]

        ax.plot(x, y, label=label)
    ax.set_title("Task 4: Center Trajectories")
    ax.legend()

    fig.savefig(fig_path)


if __name__ == "__main__":
    tids = {
        "115-20080527225031",
        "115-20080528230807",
        "115-20080618225237",
        "115-20080624022857",
        "115-20080626014331",
        "115-20080626224815",
        "115-20080701030733",
        "115-20080701225507",
        "115-20080702225600",
        "115-20080706230401",
        "115-20080707230001",
    }

    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    if not os.path.exists("./figures/task_4"):
        os.mkdir("./figures/task_4")

    trajectories = read_csv("data/geolife-cars-upd8.csv", tids)

    for epsilon in [0, 0.03, 0.1, 0.3]:
        print(f"Computing center trajectories for epsilon = {epsilon}")
        print("-----------------------------------------------------")

        simple_trajectories = {tid : ts_greedy(trajectory,epsilon) for tid, trajectory in trajectories.items()}

        # center_1 = approach_1(simple_trajectories)
        # simple_trajectories["Approach 1"] = center_1
        # average_1 = average_dtw(center_1, trajectories)
        # print(f"Average distance for Approach 1: {average_1}")

        if epsilon == 0:
            center_2 = approach_2_time(simple_trajectories)
            simple_trajectories["Approach 2"] = center_2
            average_2 = average_dtw(center_2, trajectories)
            print(f"Average distance for Approach 2: {average_2}")

        # plot(f"./figures/task_4/center_trajectories_{epsilon}.png", simple_trajectories)

        print("-----------------------------------------------------")

