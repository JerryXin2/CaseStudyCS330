import math

from utils import dtw_distance, read_csv

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


def approach_2_simple(trajectories):
    max_len = 0

    for trajectory in trajectories.values:
        if len(trajectory) > max_len:
            max_len = len(trajectory)
    
    center = []

    for t in range(max_len):
        x_tot = 0
        y_tot = 0

        for trajectory in trajectories.values():
            if t < len(trajectory):
                x_tot += trajectory[t][0]
                y_tot += trajectory[t][1]
        
        x_center = x_tot/len(trajectories.items())
        y_center = y_tot/len(trajectories.items())

        center.append((x_center, y_center))

    return center


def approach_2_complex(trajectories):
    max_len = 0

    for trajectory in trajectories.values:
        if len(trajectory) > max_len:
            max_len = len(trajectory)
    
    center = []

    for t in range(max_len):
        x_tot = 0
        y_tot = 0

        for trajectory in trajectories.values():
            t_scaled = t * len(trajectory)/max_len
            x, y = interpolate(trajectory, t_scaled)

            x_tot += x
            y_tot += y
        
        x_center = x_tot/len(trajectories.items())
        y_center = y_tot/len(trajectories.items())

        center.append((x_center, y_center))

    return center


def interpolate(trajectory, t):
    t_floor = math.floor(t)
    t_ceil = math.ceil(t)

    x = (trajectory[t_ceil][0] - trajectory[t_floor][0]) * (t - t_floor)
    y = (trajectory[t_ceil][1] - trajectory[t_floor][1]) * (t - t_floor)

    return x, y
            

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

    trajectories = read_csv("data/geolife-cars-upd8.csv", tids)

    print(approach_2_complex(trajectories))