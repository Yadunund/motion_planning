#! /usr/var/env python3

import os, sys
sys.path.insert(0, os.path.abspath(".."))
import random
import time
import numpy as np

from KdTree import KdTree
from Node import SearchNode

# For benchmarking
from scipy import spatial

def dist(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1] - b[1])**2)

def main():
    n = 100000 # number of points
    print(f"Generated {n} points")

    # generate n points
    points = []
    for i in range(n):
        x = random.uniform(-100, 100)
        y = random.uniform(-100, 100)
        points.append([x, y])
        
    s = [random.uniform(101,105), random.uniform(101, 105)]
    assert(s not in points)

    # FINDING NEAREST NEIGHBOR
    print(f"Finding nearest neighbor of {s}")
    # navie appraoch
    min_dist = np.inf
    nearest_pt = None

    start_time = time.time()
    for p in points:
        d = dist(p, s)
        if d < min_dist:
            min_dist = d
            nearest_pt = p
    assert(nearest_pt)
    end_time = time.time()
    print(f"Naive solution: {nearest_pt} found in {end_time-start_time}s")


    #KdTree
    print("#######################")
    start_time = time.time()
    t = KdTree(points[0])
    for i in range(1, len(points)):
        t.add(points[i])
    end_time = time.time()
    print(f"KdTree constructed in {end_time-start_time}s")
    start_time = time.time()
    nearest_position = t.nearest_position(s)
    end_time = time.time()
    print(f"KdTree solution: {nearest_position} found in {end_time-start_time}s")

    # Scipy
    print("#######################")
    start_time = time.time()
    scipy_tree = spatial.KDTree(points)
    end_time = time.time()
    print(f"Scipy KdTree constructed in {end_time - start_time}s")
    start_time = time.time()
    d, i = scipy_tree.query([s])
    end_time = time.time()
    print(f"Scipy tree solution: {scipy_tree.data[i[0]]} found in {end_time-start_time}s")


    # FINDING NEAREST NEIGHBORS AT DISTANCE K
    distance = 10.0
    print("#######################")
    print(f"Nearest neighbors of {s} at distance {distance}")
    
    # naive approach
    nearest_points_naive = []
    start_time = time.time()
    for p in points:
        d = dist(p, s)
        if d <= distance:
            nearest_points_naive.append(p)
    end_time = time.time()
    print(f"Naive solution found {len(nearest_points_naive)} points in {end_time-start_time}s")

    # kd tree
    start_time = time.time()
    nearest_points_tree = t.surrounding_positions(s, distance)
    end_time = time.time()
    print(f"KdTree solution found in {len(nearest_points_tree)} points in {end_time - start_time}s")
    
    # Scipy
    start_time = time.time()
    nearest_points_scipy = scipy_tree.query_ball_point(s, distance)
    end_time = time.time()
    print(f"Scipy solution found in {len(nearest_points_scipy)} points in {end_time - start_time}s")

    # Tests
    print("#######################")
    for p in nearest_points_tree:
        assert(dist(p, s) <= distance)
    for p in nearest_points_naive:
        assert p in nearest_points_tree
    print("All tests passed!")

if __name__ == '__main__':
    main()

