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
import matplotlib
import matplotlib.pyplot as plt

from OccupancyMap import OccupancyMap2D
from Dijkstra import *

def display_solution(path, map, start, goal):
    n_rows = len(map.map)
    n_cols = int(np.size(map.map)/n_rows)
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # set 0 to white, 1 to black, 2(start) to yellow, 3(goal) red and 4(path) to green
    cmap = matplotlib.colors.ListedColormap(['w', 'k', 'y', 'r', 'g'])
    map.map[start[0]][start[1]] = 2
    map.map[goal[0]][goal[1]] = 3
    
    for i in range(1, len(path) - 1):
        map.map[path[i][0]][path[i][1]] = 4

    for i in range(n_rows + 1):
        ax.axhline(i, lw = 1, color = 'k', zorder = 5)
    for i in range(n_cols + 1):
        ax.axvline(i, lw = 1, color = 'k', zorder = 5)
    ax.imshow(map.map, interpolation = 'none', cmap = cmap, extent = [0, n_rows, 0, n_cols], zorder = 0)
    ax.axis('on')
    plt.show()


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