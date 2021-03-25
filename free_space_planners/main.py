#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import time

from Map import Map

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algorithm', default='rrt', help='Algorithm to use (rrt, rrtstar)', type=str)
    parser.add_argument('--animate', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])

    map_width = 100
    map_height = 100
    map_obstacles = []

    map = Map(width=map_width, height=map_height, obstacles=map_obstacles)
    # start_time = time.time()
    # if algorithm == 'rrt':
    #     path, num_expanded, solver_steps = RRTSolver(map, start, goal)
    # elif algorithm == 'rrtstar':
    #     path, num_expanded, solver_steps = RRTStarSolver(map, start, goal)
    # else:
    #     print("Usage error: Supported algorithms are dijkstras, astar and rrt")
    #     return
    # end_time = time.time()
    # print(f"Solution found in {end_time - start_time} seconds")

if __name__ == '__main__':
    main()