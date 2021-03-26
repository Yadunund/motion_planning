#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import time

from Map import Map
from Shape import ConvexShape
from Obstacle import Obstacle
from RRT import RRTSolver

from Visualizer import display_solution

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algorithm', default='rrt', help='Algorithm to use (rrt, rrtstar)', type=str)
    parser.add_argument('--animate', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])

    map_width = 100
    map_height = 100
    start = [10, 10]
    goal = [75, 75]
    map_obstacles = []
    
    ob1 = Obstacle(ConvexShape([[25,40], [50, 60], [80, 40]]))
    ob2 = Obstacle(ConvexShape([[10,50], [10, 90], [30, 70]]))
    ob3 = Obstacle(ConvexShape([[55,95], [55, 60], [60, 60]]))
    ob4 = Obstacle(ConvexShape([[50,20], [65, 30], [80, 20]]))
    map_obstacles.append(ob1)
    map_obstacles.append(ob2)
    map_obstacles.append(ob3)
    map_obstacles.append(ob4)
    map = Map(width=map_width, height=map_height, obstacles=map_obstacles)
    
    start_time = time.time()
    if args.algorithm == 'rrt':
        path, num_expanded, expanded_nodes = RRTSolver(map, start, goal)
    # elif args.algorithm == 'rrtstar':
    #     path, num_expanded, solver_steps = RRTStarSolver(map, start, goal)
    else:
        print("Usage error: Supported algorithms are rrt")
        return
    end_time = time.time()

    print(f" {args.algorithm} ran for {end_time - start_time}s")
    display_solution(map, start, goal, path, expanded_nodes, args.algorithm)

if __name__ == '__main__':
    main()