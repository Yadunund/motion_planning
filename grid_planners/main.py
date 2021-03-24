#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import timeit
import numpy as np

from OccupancyMap import OccupancyMap2D
from Dijkstra import DijkstraSolver
from AStar import AStarSolver
from Visualizer import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n', default=10, help='Dimension of map',type= int)
    parser.add_argument('-a', '--algorithm', default='astar', help='Algorithm to use (astar, dijkstras)', type=str)
    parser.add_argument('--animate', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])

    n = max(args.n, 5)
    algorithm = args.algorithm

    obstacles = []
    start = [int(n/2), 0]
    goal = [int(n/2), int(n - 1)]
    
    # create a wall down the middle of the map
    for i in range(int(n/2)):
        obstacles.append([i, int(n/2)])

    map = OccupancyMap2D(n, n, obstacles)
    # start = (5, 1)
    # goal = (7, 8)
    start = (0, 0)
    goal = (0, n - 1)
    
    # result variables
    path = []
    num_expanded = 0
    solver_steps = []

    performance = not args.animate

    if algorithm == 'dijkstras':
        path, num_expanded, solver_steps = DijkstraSolver(map, start, goal, performance)
    elif algorithm == 'astar':
        path, num_expanded, solver_steps = AStarSolver(map, start, goal, performance)
    else:
        print("Usage error: Supported algorithms are dijkstras and astar")
        return

    if path:
        print(f'Path found from {start} to {goal} after expanding {num_expanded} nodes!')
        print(f'Path: {path}')
    else:
        print(f'No path found from {start} to {goal}')

    display_solution(path, solver_steps, map, start, goal, algorithm, args.animate)

if __name__ == '__main__':
    main()