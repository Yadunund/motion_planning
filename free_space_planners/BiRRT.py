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

from RRT import extend, ExtendResult

def get_path_distance(path:list):
    assert(len(path) > 1)
    distance = 0.0
    for i in range(1, len(path)):
        p1 = path[i]
        p0 = path[i -1]
        distance = distance + dist(p1, p0)
    return distance

def get_path(nearest_node:SearchNode, new_node:SearchNode, expanded_nodes_B:list, start, goal):
    assert(nearest_node.parent is not None)
    assert(new_node.parent is not None)
    path = []
    forward_node = new_node
    reverse_node = nearest_node
    if (start[0], start[1]) in expanded_nodes_B.keys():
        # nearest node belongs to Tree B
        reverse_node = new_node
        forward_node = nearest_node
    path_distance = forward_node.distance + dist(forward_node.position, reverse_node.position) + reverse_node.distance
    node = forward_node
    while(node.parent is not None):
        path.append(node.position)
        node = node.parent
    path.append(node.position) # start position
    path.reverse()
    
    node = reverse_node
    while(node.parent is not None):
        path.append(node.position)
        node = node.parent
    path.append(node.position) # goal position
    return path, path_distance

def display_solution(map:Map, start:list, goal:list, path:list, expanded_nodes_A:dict, expanded_nodes_B, parent=''):
    fig = plt.figure(figsize=(15,15), dpi=100)
    plt.xlim([0, map.width])
    plt.ylim([0, map.height])
    plt.title(f"Path planning with {parent} algorithm", fontsize=28)
    for obstacle in map.obstacles:
        polygon = plt.Polygon(obstacle.shape.points, True)
        plt.gca().add_line(polygon)

    # plot the expansion A
    for position, node in expanded_nodes_A.items():
        plt.plot([position[0]], [position[1]], 'go')
        if node.parent is not None:
            edge = [node.position, node.parent.position]
            line = plt.Polygon(edge, closed=None, fill=None, edgecolor='g')
            plt.gca().add_line(line)
    # plot the expansion B
    for position, node in expanded_nodes_B.items():
        plt.plot([position[0]], [position[1]], 'ro')
        if node.parent is not None:
            edge = [node.position, node.parent.position]
            line = plt.Polygon(edge, closed=None, fill=None, edgecolor='r')
            plt.gca().add_line(line)

    if path:
      line = plt.Polygon(path, closed=None, fill=None, edgecolor='k', linewidth = 5.0)
      plt.gca().add_line(line)

    plt.plot([start[0]], [start[1]], 'yo') # start
    plt.plot([goal[0]], [goal[1]], 'bo')

    plt.show()

def BiRRTSolver(map:Map, start:list, goal:list, steps=False):
    start_time = time.time()
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
        if extend(tree_A, new_node, expanded_nodes_A, max_step, goal_node, goal_radius, map) != ExtendResult.Trapped:
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
    display_solution(map, start, goal, path, expanded_nodes_A, expanded_nodes_B, "BiRRT")

    return path, num_expanded, {**expanded_nodes_A, **expanded_nodes_B}




