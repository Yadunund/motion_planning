#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import timeit
import numpy as np

from OccupancyMap import OccupancyMap2D
from Dijkstra import DijkstraSolver
from AStar import AStarSolver
from RRT import RRTSolver
from Visualizer import *

import time

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--n', default=10, help='Dimension of map',type= int)
    parser.add_argument('-a', '--algorithm', default='astar', help='Algorithm to use (astar, dijkstras)', type=str)
    parser.add_argument('--animate', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])

    n = max(args.n, 5)
    algorithm = args.algorithm

    obstacles = []   
    # create a wall 3/4 down the middle of the map
    v_wall_index = int(n * 0.75)
    for i in range(v_wall_index):
        obstacles.append([i, int(n/2)])
    
    # create a horizontal wall
    # v_wall_index = min(v_wall_index, n - 1)
    # for i in range(int(n/2), n - 2):
    #     obstacles.append([v_wall_index, i])

    map = OccupancyMap2D(n, n, obstacles)

    start = (0, 0)
    goal = (0, int(0.75 * n))
    
    # result variables
    path = []
    num_expanded = 0
    solver_steps = []

    performance = not args.animate

    start_time = time.time()
    if algorithm == 'dijkstras':
        path, num_expanded, solver_steps = DijkstraSolver(map, start, goal, performance)
    elif algorithm == 'astar':
        path, num_expanded, solver_steps = AStarSolver(map, start, goal, performance)
    elif algorithm == 'rrt':
        path, num_expanded, solver_steps = RRTSolver(map, start, goal)
    else:
        print("Usage error: Supported algorithms are dijkstras, astar and rrt")
        return
    end_time = time.time()
    print(f"Solution found in {end_time - start_time} seconds")

    if path:
        print(f'Path found from {start} to {goal} after expanding {num_expanded} nodes!')
        print(f'Path: {path}')
    else:
        print(f'No path found from {start} to {goal}')

    display_solution(path, solver_steps, map, start, goal, algorithm, args.animate)

if __name__ == '__main__':
    main()