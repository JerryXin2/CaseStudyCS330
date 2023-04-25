import os
import copy
import random
import matplotlib.pyplot as plt

from center import approach_2
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
            if partition:
                new_center = approach_2({tid : trajectories[tid] for tid in partition})
                new_centers.append(new_center)
            else:
                new_center = seed_fn(trajectories)[0]
                new_centers.append(new_center)

        # If the algorithm has converged, stop
        if new_centers == centers:
            break

        # Otherwise, run the next iteration with the new centers
        else:
            centers = new_centers
            
    return centers, costs


def random_seed(trajectories, k = 1):
    
    return random.sample(list(trajectories.values()), k)


def proposed_seed(trajectories, k = 1):
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


def plot_1(fig_path, k, random_cost, proposed_cost):
    fig, ax = plt.subplots()

    ax.plot(k, random_cost, label = "Random Seeding")
    ax.plot(k, proposed_cost, label = "Proposed Seeding")
    ax.set_xlabel("k")
    ax.set_ylabel("cost of clustering")
    ax.set_title("Task 5: k vs. cost of clustering")
    ax.legend()

    fig.savefig(fig_path)


def plot_2(fig_path, centers):
    fig, ax = plt.subplots()

    label = 0
    for center in centers:
        x = [c[0] for c in center]
        y = [c[1] for c in center]

        ax.plot(x, y, label = label)
        
        label += 1
    ax.set_title("Task 5: Cluster Centers")

    fig.savefig(fig_path)


def plot_3(fig_path, random_cost, proposed_cost):
    fig, ax = plt.subplots()

    random_iters = [i + 1 for i in range(len(random_cost))]
    proposed_iters = [i + 1 for i in range(len(proposed_cost))]

    ax.plot(random_iters, random_cost, label = "Random Seeding")
    ax.plot(proposed_iters, proposed_cost, label = "Proposed Seeding")
    ax.set_xlabel("iteration number")
    ax.set_ylabel("cost of clustering")
    ax.set_title("Task 5: iteration number vs. cost of clustering")
    ax.legend()

    fig.savefig(fig_path)


if __name__ == "__main__":
    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    if not os.path.exists("./figures/task_5"):
        os.mkdir("./figures/task_5")

    trajectories = read_csv("data/geolife-cars-upd8.csv")
    simple_trajectories = {tid : ts_greedy(trajectory, 0.1) for tid, trajectory in trajectories.items()}

    ITERS = 3
    K_VAL = 12
    T_MAX = 100

    random_cost = []
    proposed_cost = []
    for i, k in enumerate([4, 6, 8, 10, 12]):
        print(f"Running Lloyd's algorithm with random seeding and {k} clusters:")
        print("-----------------------------------------------------")

        random_cost.append(0)
        for iter in range(ITERS):
            centers, costs = lloyds(simple_trajectories, random_seed, k, T_MAX)
            random_cost[i] += costs[-1]

            print(f"Iteration {iter}: {costs[-1]}")

        print(f"Average {iter}: {random_cost[i]/ITERS}")
        print("-----------------------------------------------------")

        print(f"Running Lloyd's algorithm with proposed seeding and {k} clusters")
        print("-----------------------------------------------------")

        proposed_cost.append(0)
        for iter in range(ITERS):
            centers, costs = lloyds(simple_trajectories, proposed_seed, k, T_MAX)
            proposed_cost[i] += costs[-1]

            print(f"Iteration {iter}: {costs[-1]}")

        print(f"Average {iter}: {proposed_cost[i]/ITERS}")
        print("-----------------------------------------------------")
    random_avg = [c/ITERS for c in random_cost]
    proposed_avg = [c/ITERS for c in proposed_cost]
    plot_1("./figures/task_5/k_cost.png", [4, 6, 8, 10, 12], random_avg, proposed_avg)

    random_cost = []
    proposed_cost = []
    for iter in range(ITERS):
        centers, costs = lloyds(simple_trajectories, random_seed, K_VAL, T_MAX)
        random_cost.append(costs)

        centers, costs = lloyds(simple_trajectories, proposed_seed, K_VAL, T_MAX)
        proposed_cost.append(costs)

        if iter == 0:
            plot_2("./figures/task_5/", centers)

    max_len = max(len(random_cost[0]), len(random_cost[1]), len(random_cost[2]))
    if len(random_cost[0]) < max_len:
        random_cost[0] + (random_cost[0][-1] * (max_len - len(random_cost[0])))
    if len(random_cost[1]) < max_len:
        random_cost[1] + (random_cost[1][-1] * (max_len - len(random_cost[1])))   
    if len(random_cost[2]) < max_len:
        random_cost[2] + (random_cost[2][-1] * (max_len - len(random_cost[2])))
    random_avg = [(random_cost[0][i] + random_cost[1][i] + random_cost[2][i])/3 for i in range(len(random_cost[0]))]

    max_len = max(len(proposed_cost[0]), len(proposed_cost[1]), len(proposed_cost[2]))
    if len(proposed_cost[0]) < max_len:
        proposed_cost[0] + (proposed_cost[0][-1] * (max_len - len(proposed_cost[0])))
    if len(proposed_cost[1]) < max_len:
        proposed_cost[1] + (proposed_cost[1][-1] * (max_len - len(proposed_cost[1])))   
    if len(proposed_cost[2]) < max_len:
        proposed_cost[2] + (proposed_cost[2][-1] * (max_len - len(proposed_cost[2])))
    proposed_avg = [(proposed_cost[0][i] + proposed_cost[1][i] + proposed_cost[2][i])/3 for i in range(len(proposed_cost[0]))]

    plot_3("./figures/task_5/", random_avg, proposed_avg)

