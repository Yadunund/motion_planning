from KdTree import KdTree
from Node import SearchNode
from Map import Map

from utils import dist, in_point_collision, in_line_collision

import numpy as np
import matplotlib.pyplot as plt

import math
import threading
import time
import random
import copy

from RRT import ExtendResult
from RRTStar import extend
from BiRRT import get_path, display_solution

def BiRRTStarSolver(map:Map, start:list, goal:list, steps=False, informed=False):
    start_time = time.time()
    goal_radius = 2.5 # meters
    max_step = 10.0
    neighborhood = 50.0
    n = 3000
  
    if in_point_collision(start, map):
        print(f"[error] start {start} is on an obstacle")
        return
    if in_point_collision(goal, map):
        print(f"[error] goal {goal} is on an obstacle")
        return

    if dist(start, goal) <= goal_radius:
        print(f"Start is already within goal radius")
        return
    
    path = []
    num_expanded = 0

    # TreeA
    expanded_nodes_A = {}
    tree_A = KdTree(start)

    # TreeB
    expanded_nodes_B = {}
    tree_B = KdTree(goal)

    new_node = None
    found = False
    path_distance = 0.0

    start_node = SearchNode(start, None, 0.0)
    goal_node = SearchNode(goal, None, 0.0)

    expanded_nodes_A[(start_node.position[0], start_node.position[1])] = start_node
    expanded_nodes_B[(goal_node.position[0], goal_node.position[1])] = goal_node

    while (num_expanded < n):
        num_expanded = num_expanded + 1
        random_position = map.random_position()
        new_node = SearchNode(random_position)
        if (in_point_collision(new_node.position, map)):
            continue        
        # Extend Tree A towards new node
        if extend(tree_A, new_node, expanded_nodes_A, max_step, neighborhood, goal_node, goal_radius, map)[0] != ExtendResult.Trapped:
        # check if nearest node in Tree B is within max_step
            nearest_position = tree_B.nearest_position(new_node.position)
            if dist(nearest_position, new_node.position) <= max_step and (not in_line_collision([nearest_position, new_node.position], map)):
                nearest_node = expanded_nodes_B[(nearest_position[0], nearest_position[1])]
                path, path_distance = get_path(nearest_node, new_node, expanded_nodes_B, start, goal)
                break
        # swap
        else:
            tmp = expanded_nodes_A
            expanded_nodes_A = expanded_nodes_B
            expanded_nodes_B = tmp
            tmp = start_node
            start_node = goal_node
            goal_node = tmp
            tmp = tree_A
            tree_A = tree_B
            tree_B = tmp


    finish_time = time.time()
    print(f"Path from {start} to {goal} found with distance {path_distance} after expanding {num_expanded} nodes in {finish_time - start_time}s")
    display_solution(map, start, goal, path, expanded_nodes_A, expanded_nodes_B, "BiRRTStar")

    return path, num_expanded, {**expanded_nodes_A, **expanded_nodes_B}




