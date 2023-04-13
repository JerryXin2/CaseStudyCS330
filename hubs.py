import os
import csv
import sys
import math
import time
import matplotlib.pyplot as plt
import matplotlib.patches as ptc

def read_csv(csv_path):
    """Returns the list of points and their x and y boundaries."""
    points = []
    xmax = 0
    ymax = 0
    xmin = sys.maxsize
    ymin = sys.maxsize

    with open(csv_path) as file:
        reader = csv.reader(file, delimiter=",")

        next(file)
        for row in reader:
            points.append((float(row[2]), float(row[3])))
            xmax = max(xmax, float(row[2]))
            ymax = max(ymax, float(row[3]))
            xmin = min(xmin, float(row[2]))
            ymin = min(ymin, float(row[3]))

    xmax = math.ceil(xmax)
    ymax = math.ceil(ymax)
    xmin = math.floor(xmin)
    ymin = math.floor(ymin)

    return points, xmax, ymax, xmin, ymin

def preprocess(points, xmax, ymax, xmin, ymin, binwidth, binheight):
    """Inserts each point into rectangular bins of width binwidth and height binheight.  Returns the rectangular bins sorted by density."""
    xbins = math.ceil((xmax - xmin)/binwidth)
    ybins = math.ceil((ymax - ymin)/binheight)

    bins = {}
    for xbin in range(xbins):
        for ybin in range(ybins):
            bins[(xbin, ybin)] = 0

    for point in points:
        xbin = (point[0] - xmin)//binwidth
        ybin = (point[1] - ymin)//binheight
        bins[(xbin, ybin)] += 1   

    # Sorts the bins by density
    bins = dict(sorted(bins.items(), key = lambda item: get_density(((item[0][0] + 0.5) * binwidth + xmin, (item[0][1] + 0.5) * binheight + ymin), xmin, ymin, xbins, ybins, bins, binwidth, binheight), reverse = True))

    return bins

def get_density(point, xmin, ymin, xbins, ybins, bins, binwidth, binheight):
    """Returns the sum of the points within a bin and its 8 surrounding bins"""
    xpoint, ypoint = point
    xbin, ybin = (xpoint - xmin)//binwidth, (ypoint - ymin)//binheight

    density = 0
    # Adds the number of points in the bin that contains the point with the number of points in the surrounding 8 bins
    for x in range(int(max(0, xbin - 1)), int(min(xbins, xbin + 2))):
        for y in range(int(max(0, ybin - 1)), int(min(ybins, ybin + 2))):
            density += bins[(x, y)]

    return density

def get_hubs(xmin, ymin, bins, binwidth, binheight, k, r):
    """Iterates through the sorted bins, adding the middle of each bin to a list of hubs if it is at least r away from existing hubs.  Returns a list of k hubs."""
    hubs = []

    for bin in bins.keys():
        xbin, ybin = bin
        hub = (xbin + 0.5) * binwidth + xmin, (ybin + 0.5) * binheight + ymin

        # Check if the candidate hub is at least r away from all selected hubs
        if all(distance(hub, p) >= r for p in hubs):
            hubs.append(hub)

        if len(hubs) == k:
            return hubs
        
    return hubs

def distance(p, q):
    """Returns the Euclidean distance between p and q."""
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2)**0.5

def plot(fig_path, points, hubs, r):
    """Generates and saves a visualization of points and hubs."""
    xpoints = []
    ypoints = []
    xhubs = []
    yhubs = []
    
    for point in points:
        xpoints.append(point[0])
        ypoints.append(point[1])
    for hub in hubs:
        xhubs.append(hub[0])
        yhubs.append(hub[1])
    
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.scatter(xpoints, ypoints, marker = ".", s = 1, c = "b", alpha = 0.1, label = "Points")
    ax.scatter(xhubs, yhubs, marker = "s", s = 2, c = "r", label = "Hubs")
    ax.legend()

    for hub in hubs:
        circle = ptc.Circle(hub, r, color = "r", fill = False)
        ax.add_patch(circle)

    fig.savefig(fig_path, dpi = 500)
    
def experiment(csv_path, fig_path, binwidth, binheight, k, r):
    """Runs an experiment with given input variables.  Returns the runtime of preprocessing and getting hubs."""
    points, xmax, ymax, xmin, ymin = read_csv(csv_path)
    start = time.time()
    bins = preprocess(points, xmax, ymax, xmin, ymin, binwidth, binheight)
    hubs = get_hubs(xmin, ymin, bins, binwidth, binheight, k, r)
    runtime = time.time() - start
    plot(fig_path, points, hubs, r)

    return runtime

if __name__ == "__main__":
    """Runs the list of experiments designated in the case study description"""
    csv_path = "./data/geolife-cars.csv"
    
    binwidth = 1
    binheight = 1
    iters = 5

    if not os.path.exists("./figures"):
        os.mkdir("./figures")
    if not os.path.exists("./figures/task_1"):
        os.mkdir("./figures/task_1")

    experiment(csv_path, "./figures/task_1/geolife-cars_10_8.png", binwidth, binheight, 10, 8)

    # Naming convention: "./figures/task_1/dataset_k_r.png"
    for k in [5, 10, 20, 40]:
        print(f"geolife-cars, k = {k}, r = 2:")
        print("-----------------------------")
        total = 0
        for iter in range(iters):
            runtime = experiment(csv_path, f"./figures/task_1/geolife-cars_{k}_2.png", binwidth, binheight, k, 2)
            print(runtime)
            total += runtime
        print(f"Average runtime over {iters} iterations: {total/iters}")
        
    for path in ["geolife-cars-ten-percent", "geolife-cars-thirty-percent", "geolife-cars-sixty-percent", "geolife-cars"]:
        print(f"{path}, k = 10, r = 8:")
        print("-----------------------------")
        total = 0
        for iter in range(iters):
            runtime = experiment(f"data/{path}.csv", f"./figures/task_1/{path}_10_8.png", binwidth, binheight, 10, 8)
            print(runtime)
            total += runtime
        print(f"Average runtime over {iters} iterations: {total/iters}")