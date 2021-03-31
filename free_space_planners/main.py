#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import time

from Map import Map
from Shape import ConvexShape
from Obstacle import Obstacle
from RRT import RRTSolver
from RRTStar import RRTStarSolver

from Visualizer import display_solution

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--algorithm', default='rrt', help='Algorithm to use (rrt, rrtstar)', type=str)
    parser.add_argument('--animate', action='store_true', default=False)
    args = parser.parse_args(sys.argv[1:])

    map_width = 200
    map_height = 200
    start = [60, 80]
    goal = [125, 125]
    map_obstacles = []
    
    ob1 = Obstacle(ConvexShape([[75,90], [100, 110], [130, 90]]))
    ob2 = Obstacle(ConvexShape([[60,110], [60, 140], [80, 120]]))
    ob3 = Obstacle(ConvexShape([[85,115], [110, 160], [115, 115]]))
    ob4 = Obstacle(ConvexShape([[140,100], [125, 120], [160, 100]]))
    map_obstacles.append(ob1)
    map_obstacles.append(ob2)
    map_obstacles.append(ob3)
    map_obstacles.append(ob4)
    map = Map(width=map_width, height=map_height, obstacles=map_obstacles)
    
    print(f'Solving using {args.algorithm}...')
    start_time = time.time()
    if args.algorithm == 'rrt':
        path, num_expanded, expanded_nodes = RRTSolver(map, start, goal)
    elif args.algorithm == 'rrtstar':
        path, num_expanded, expanded_nodes = RRTStarSolver(map, start, goal)
    elif args.algorithm == 'irrtstar':
          path, num_expanded, expanded_nodes = RRTStarSolver(map, start, goal, informed=True)
    else:
        print("Usage error: Supported algorithms are rrt")
        return
    end_time = time.time()

    print(f" {args.algorithm} ran for {end_time - start_time}s")
    display_solution(map, start, goal, path, expanded_nodes, args.algorithm)

if __name__ == '__main__':
    main()