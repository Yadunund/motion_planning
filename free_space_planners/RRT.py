from KdTree import KdTree
from Node import SearchNode
from Map import Map

from utils import dist, in_point_collision, in_line_collision

import math
import threading
import time
import numpy as np
from enum import Enum

class ExtendResult(Enum):
    Trapped = 1
    Advanced = 2
    Reached = 3

def extend(tree, new_node, expanded_nodes, max_step, goal_node, goal_radius, map):
    result = ExtendResult.Reached    
    # get nearest node
    nearest_position = tree.nearest_position(new_node.position)
    nearest_node = expanded_nodes[(nearest_position[0], nearest_position[1])]

    # check if new_node is within step distance from nearest_node
    distance = dist(new_node.position, nearest_node.position)
    new_node.distance = distance + nearest_node.distance
    if distance > max_step:
        x1, y1 = nearest_node.position
        x2, y2 = new_node.position
        v = [x2 - x1, y2 - y1]
        magnitude_v = math.sqrt(v[0]**2 + v[1]**2)
        u = [v[0]/magnitude_v, v[1]/magnitude_v]
        new_point = [x1 + max_step*u[0], y1 + max_step*u[1]]
        new_dist = dist(new_point, nearest_node.position)
        new_node.position = new_point
        new_node.distance = new_dist + nearest_node.distance
        if in_line_collision([new_node.position, nearest_node.position], map):
            return ExtendResult.Trapped
        result = ExtendResult.Advanced

    new_node.parent = nearest_node
    expanded_nodes[(new_node.position[0], new_node.position[1])] = new_node

    # check if new_node is within goal boundary
    dist_to_goal = dist(new_node.position, goal_node.position)
    total_distance = new_node.distance + dist_to_goal
    if dist_to_goal <= goal_radius and total_distance < goal_node.distance:
        goal_node.parent = new_node
        goal_node.distance = total_distance

    # add new node to tree
    tree.add(new_node.position)

    return result

def RRTSolver(map:Map, start:list, goal:list, steps=False):
    goal_radius = 2.5 # meters
    max_step = 10.0
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
    expanded_nodes = {}

    root = SearchNode(start)
    expanded_nodes[(root.position[0], root.position[1])] = root
    goal_node = SearchNode(goal, None, np.inf)
    tree = KdTree(start)
    found = False

    while (num_expanded < n):
        random_position = map.random_position() if num_expanded % 10 != 0 else goal_node.position
        new_node = SearchNode(random_position)
        if (in_point_collision(new_node.position, map)):
            continue
        extend(tree, new_node, expanded_nodes, max_step, goal_node, goal_radius, map)
        num_expanded = num_expanded + 1
        if (goal_node.parent is not None):
            found = True
            break

    if (goal_node.parent is not None):
        print(f"Path from {start} to {goal} found with distance {goal_node.distance} after expanding {num_expanded} nodes")
        node = goal_node
        while (node.parent != None):
            path.append(node.position)
            node = node.parent
        
        path.append(start)

        path.reverse()

    return path, num_expanded, expanded_nodes




