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

from RRT import ExtendResult
from RRTStar import RotationToWorldFrame, SampleUnitBall, InformedSample

import dubins # python3 -m pip install dubins

def extend(tree, new_node, expanded_nodes, max_step, neighborhood, goal_node, goal_radius, map, turning_radius):
    result = ExtendResult.Reached
    nearest_position = tree.nearest_position(new_node.position)
    nearest_node = expanded_nodes[(nearest_position[0], nearest_position[1], nearest_position[2])]

    path = dubins.shortest_path(nearest_node.position, new_node.position, turning_radius)
    distance = path.path_length()
    new_node.distance = distance + nearest_node.distance
    new_node.path = path

    # check if new_node is within step distance from nearest_node
    if distance > max_step:
        x1, y1, yaw1 = nearest_node.position
        x2, y2, yaw2 = new_node.position
        v = [x2 - x1, y2 - y1]
        magnitude_v = math.sqrt(v[0]**2 + v[1]**2)
        u = [v[0]/magnitude_v, v[1]/magnitude_v]
        new_point = [x1 + max_step*u[0], y1 + max_step*u[1], yaw2]
        new_path = dubins.shortest_path(nearest_node.position, new_point, turning_radius)
        new_dist = new_path.path_length()
        new_node.position = new_point
        new_node.distance = new_dist + nearest_node.distance
        new_node.path = new_path
        result = ExtendResult.Advanced

    if in_line_collision([new_node.position, nearest_node.position], map):
        return ExtendResult.Trapped, goal_node.distance

    # Assign parent based on lowest distance among neighborhood points
    new_node.parent = nearest_node
    surrounding_positions = tree.surrounding_positions(new_node.position, neighborhood)
    for position in surrounding_positions:
        node = expanded_nodes[(position[0], position[1], position[2])]
        neighbor_path = dubins.shortest_path(node.position, new_node.position, turning_radius)
        neighbor_distance = neighbor_path.path_length()
        if node.distance + neighbor_distance < new_node.distance:
            if not in_line_collision([node.position, new_node.position], map):
                new_node.parent = node
                new_node.distance = node.distance + neighbor_distance
                new_node.path = neighbor_path

    # Rewire surrounding nodes to new_node if feasible
    for position in surrounding_positions:
        node = expanded_nodes[(position[0], position[1], position[2])]
        neighbor_path = dubins.shortest_path(new_node.position, node.position, turning_radius)
        neighbor_distance = neighbor_path.path_length()
        if new_node.distance + neighbor_distance < node.distance:
            if not in_line_collision([node.position, new_node.position], map):
                node.parent = new_node
                node.distance = new_node.distance + neighbor_distance
                node.path = neighbor_path
    
    # check if new_node is within goal boundary
    goal_path = dubins.shortest_path(new_node.position, goal_node.position, turning_radius)
    dist_to_goal = goal_path.path_length()
    total_distance = new_node.distance + dist_to_goal
    if dist_to_goal <= goal_radius and total_distance < goal_node.distance:
        goal_node.parent = new_node
        goal_node.distance = total_distance
        goal_node.path = goal_path

    # add new node to graph and tree
    expanded_nodes[(new_node.position[0], new_node.position[1], new_node.position[2])] = new_node
    tree.add(new_node.position)
    
    return (result, goal_node.distance)

def display_solution(map:Map, start:list, goal:list, dubins_path:list, expanded_nodes, parent=''):
    fig = plt.figure(figsize=(15,15), dpi=100)
    plt.xlim([0, map.width])
    plt.ylim([0, map.height])
    plt.title(f"Path planning with {parent} algorithm", fontsize=28)
    for obstacle in map.obstacles:
        polygon = plt.Polygon(obstacle.shape.points, True)
        plt.gca().add_line(polygon)

    # plot the expansion A
    for position, node in expanded_nodes.items():
        plt.plot([position[0]], [position[1]], 'go')
        if node.parent is not None:
            path = node.path
            path_points, _ = path.sample_many(0.1)
            x = [p[0] for p in path_points]
            y = [p[1] for p in path_points]
            plt.plot(x, y, 'g-', linewidth=0.5)

    for path in dubins_path:
        path_points, _ = path.sample_many(0.1)
        x = [p[0] for p in path_points]
        y = [p[1] for p in path_points]
        plt.plot(x, y, 'k-', linewidth=5)

    plt.plot([start[0]], [start[1]], 'yo') # start
    plt.plot([goal[0]], [goal[1]], 'bo')

    plt.show()

def DubinsRRTStarSolver(map:Map, start:list, goal:list, steps=False, informed=False):
    start_time = time.time()
    goal_radius = 5.0 # meters
    max_step = 20.0
    neighborhood = 40.0
    n = 3000
    turning_radius = 1.0

    start_yaw = np.pi/2
    goal_yaw = np.pi/2
    start.append(start_yaw)
    goal.append(goal_yaw)

    # Constants for informed sampling
    c_best = np.inf # cost to goal
    c_min = dist(goal, start)
    x_center = np.array([0.5 * (start[0] + goal[0]), 0.5 * (start[1] + goal[1]), 0.0])
    C = RotationToWorldFrame(start, goal, c_min)

    if in_point_collision(start[:2], map):
        print(f"[error] start {start} is on an obstacle")
        return
    if in_point_collision(goal[:2], map):
        print(f"[error] goal {goal} is on an obstacle")
        return

    if dist(start, goal) <= goal_radius:
        print(f"Start is already within goal radius")
        return
    
    path = []
    dubins_path = [] # list of dubins curves
    num_expanded = 0
    expanded_nodes = {}

    root = SearchNode(start)
    goal_node = SearchNode(goal, None, np.inf)
    expanded_nodes[(root.position[0], root.position[1], root.position[2])] = root
    tree = KdTree(start)

    while (num_expanded < n):

        if num_expanded % 10 == 0:
            random_position = goal_node.position[:2]
        elif not informed:
            random_position = map.random_position()
        else:
            random_position = InformedSample(c_best, c_min, x_center, C, map)
        # Append random yaw
        random_position.append(random.uniform(-np.pi, np.pi))
        
        # get nearest node
        new_node = SearchNode(random_position)
        result, c_best = extend(tree, new_node, expanded_nodes, max_step, neighborhood, goal_node, goal_radius, map, turning_radius)
        num_expanded = num_expanded + 1

    finish_time = time.time()
    print(f"Kinodynamic RRT* ran for {finish_time - start_time}s")
    if (goal_node.parent is not None):
        print(f"Path from {start} to {goal} found with distance {goal_node.distance} after expanding {num_expanded} nodes")
        node = goal_node
        while (node.parent != None):
            path.append(node.position[:2])
            dubins_path.append(node.path)
            node = node.parent
        
        path.append(start)
        path.reverse()
    else:
        print("Solution not found!")

    display_solution(map, start, goal, dubins_path, expanded_nodes, 'KinodynamicRRT*')

    return path, num_expanded, expanded_nodes




