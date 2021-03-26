#! /usr/var/env python3

import os, sys
sys.path.insert(0, os.path.abspath(".."))
import random
import time
import numpy as np

from KdTree import KdTree
from Node import SearchNode

def dist(a, b):
    return np.sqrt((a[0]-b[0])**2 + (a[1] - b[1])**2)

def main():
    n = 100000 # number of points

    # generate n points
    points = []
    for i in range(n):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        points.append([x, y])
        
    s = [random.randint(0,100), random.randint(0, 100)]

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
    print(f"Navie solution: {nearest_pt} found in {end_time-start_time}s")


    #KdTree
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


if __name__ == '__main__':
    main()

