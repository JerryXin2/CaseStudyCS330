import os
import copy
import random
import matplotlib.pyplot as plt

from center import approach_2_time
from utils import dtw_distance, read_csv, ts_greedy

def lloyds(trajectories, seed_fn, k, t_max):
    # Initialize centers via seeding algorithm
    centers = seed_fn(trajectories, k)

    # Array for costs
    costs = []

    # Run for t_max iterations
    for t in range(t_max):
        # Initialize cost for this iteration
        costs.append(0)

        # Array for partitiions
        partitions = [[] for _ in centers]

        # Sort trajectories into partitions
        for tid, trajectory in trajectories.items():
            min_dist = float("inf")
            min_center = None

            for i, center in enumerate(centers):
                dist = dtw_distance(trajectory, center)
                if dist < min_dist:
                    min_dist = dist
                    min_center = i

            partitions[min_center].append(tid)

            # Update cost
            costs[t] += min_dist

        # Compute new centers
        new_centers = []
        for partition in partitions:
            new_center = approach_2_time({tid : trajectories[tid] for tid in partition})
            new_centers.append(new_center)

        # If the algorithm has converged, stop
        if new_centers == centers:
            break

        # Otherwise, run the next iteration with the new centers
        else:
            centers = new_centers
            
    return centers, costs


def random_seed(trajectories, k):
    
    return random.sample(list(trajectories.values()), k)


def weighted_seed(trajectories, k):
    # Array for centers
    seed = []

    # Select the first center using a uniform random distribution
    seed.append(random.choice(list(trajectories.keys())))

    # Dictionary for the minimum distance to already-selected centers
    min_dist = {tid : float("inf") for tid in trajectories.keys()}
    
    # Select remaining centers
    for _ in range(k - 1):

        # Compute minimum distance to already-selected centers
        for tid, trajectory in trajectories.items():
            for center in seed:
                dist = dtw_distance(trajectory, trajectories[center])
                if dist**2 < min_dist[tid]:
                    min_dist[tid] = dist**2

        # Select the next center using a distribution weighted by the minimum distance
        weights = [min_dist[tid] for tid in trajectories.keys()]
        seed.append(random.choices(list(trajectories.keys()), weights = weights)[0])

    return [trajectories[tid] for tid in seed]

if __name__ == "__main__":
    tids = {
        "115-20080527225031",
        "115-20080528230807",
        "115-20080618225237",
        "115-20080624022857",
        "115-20080626014331",
    }

    trajectories = read_csv("data/geolife-cars-upd8.csv", tids)

    simple_trajectories = {tid : ts_greedy(trajectory, 0.3) for tid, trajectory in trajectories.items()}

    print(lloyds(simple_trajectories, weighted_seed, 1, 10))



