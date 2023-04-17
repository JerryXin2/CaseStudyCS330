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

def approach_2_simple(trajectories):
    new_traj = []
    max = 0
    for tid, trajectory in trajectories.items():
        if(len(trajectory) > max):
            max = len(trajectory)
    for i in range(max+1):
        for tid, trajectory in trajectories.items():
            sumA = 0
            countA = 0
            sumB = 0
            countB = 0
            if trajectory[i][0] != None:
                sumA += trajectory[i][0]
                countA+=1
            if trajectory[i][1] != None:
                sumB += trajectory[i][1]
                countB+=1
        new_traj.add((sumA/countA, sumB/countB))
    return new_traj



