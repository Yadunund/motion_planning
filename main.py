#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:49:15 2020

@author: yadu
"""

import sys
import argparse
import numpy as np

from OccupancyMap import OccupancyMap2D
from Dijkstra import *

def display_solution(path, map):
    solution_map = map
    for p in path:
        solution_map.map[p[0]][p[1]] = 6
    solution_map.display_map()

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument()
    n = 10
    obstacles = []
    start = [int(n/2), 0]
    goal = [int(n/2), int(n - 1)]
    
    # create a wall down the middle of the map except for bottom-most row
    for i in range(int(n/2)):
        obstacles.append([i, int(n/2)])
    
        
    map = OccupancyMap2D(n, obstacles)
    
    #solve using Dijkstra
    start = (0, 0)
    goal = (0, 8)
    path, num_expanded = DijkstraSolver(map, start, goal)

    if path:
        print(f'Path found from {start} to {goal}!')
        print(f'Expanded {num_expanded} nodes')
        print(f'Path: {path}')
        display_solution(path, map)
    else:
        print(f'No path found from {start} to {goal}')
        
if __name__ == '__main__':
    main()