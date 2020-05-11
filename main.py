#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:49:15 2020

@author: yadu
"""

import sys
import argparse
import timeit
import numpy as np

from OccupancyMap import OccupancyMap2D
from Dijkstra import *
from Visualizer import *

def main():
    
    n = 100
    obstacles = []
    start = [int(n/2), 0]
    goal = [int(n/2), int(n - 1)]
    
    # create a wall down the middle of the map except for bottom-most row
    for i in range(int(n/2)):
        obstacles.append([i, int(n/2)])

    map = OccupancyMap2D(n, obstacles)
    
    #solve using Dijkstra
    # start = (5, 1)
    # goal = (7, 8)
    start = (0, 0)
    goal = (0, n - 1)
    
    path, num_expanded = DijkstraSolver(map, start, goal)
    display_solution(path, map, start, goal)

    if path:
        print(f'Path found from {start} to {goal} after expanding {num_expanded} nodes!')
        print(f'Path: {path}')
    else:
        print(f'No path found from {start} to {goal}')
        
if __name__ == '__main__':
    main()