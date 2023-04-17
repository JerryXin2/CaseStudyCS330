from utils import dtw_distance

def approach_1(trajectories):
    dtw_distances = {}

    for tid, trajectory in trajectories.items():
        dtw_distances[tid] = 0

        for tid2, trajectory2 in trajectories.items():
            if tid != tid2:
                dtw_distances[tid] += dtw_distance(trajectory, trajectory2)
    
    min = float("inf")
    min_tid = None
    for tid, dist in dtw_distances.items():
        if dist < min:
            min = dist
            min_tid = tid
    
    return trajectories[min_tid]

def approach_2(trajectories):
    
