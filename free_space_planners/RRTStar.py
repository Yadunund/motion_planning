from KdTree import KdTree
from Node import SearchNode
from Map import Map

from utils import dist, in_point_collision, in_line_collision

import numpy as np

import math
import threading
import time
import random

def naive_surrounding_positions(position, distance, expanded_nodes):
    surrounding_positions = []
    for p, n in expanded_nodes.items():
        if dist(n.position, position) <= distance:
            surrounding_positions.append(n.position)
    return surrounding_positions

def RotationToWorldFrame(start, goal, L):
    a1 = np.array([[(goal[0] - start[0]) / L],
                    [(goal[1] - start[1]) / L], [0.0]])
    e1 = np.array([[1.0], [0.0], [0.0]])
    M = a1 @ e1.T
    U, _, V_T = np.linalg.svd(M, True, True)
    C = U @ np.diag([1.0, 1.0, np.linalg.det(U) * np.linalg.det(V_T.T)]) @ V_T
    return C

def SampleUnitBall():
    theta = 2 * np.pi * random.uniform(0, 1)
    r = random.uniform(0, 1)
    return np.array([r*np.cos(theta), r*np.sin(theta), 0.0])

def InformedSample(c_max, c_min, x_center, C, map:Map):
    if c_max != np.inf: # if a path to goal has been found we sample from the prolate  hyperspheroid
        r1 = c_max / 2.0
        rn = math.sqrt(c_max **2 - c_min **2) / 2.0
        L = np.diag([r1, rn, rn])
        x_ball = SampleUnitBall()
        x_rand = np.dot(np.dot(C, L), x_ball) + x_center
        return [x_rand[0], x_rand[1]]
        
    else:
        return map.random_position()


def RRTStarSolver(map:Map, start:list, goal:list, steps=False, informed=False):
    goal_radius = 2.5 # meters
    max_step = 10.0
    neighborhood = 10.0
    n = 7000

    # Constants for informed sampling
    c_best = np.inf # cost to goal
    c_min = dist(goal, start)
    x_center = np.array([0.5 * (start[0] + goal[0]), 0.5 * (start[1] + goal[1]), 0.0])
    C = RotationToWorldFrame(start, goal, c_min)

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
    goal_node = SearchNode(goal, None, np.inf)
    expanded_nodes[(root.position[0], root.position[1])] = root
    tree = KdTree(start)

    found = False
    while (num_expanded < n):
        if not informed:
            random_position = map.random_position()
        else:
            random_position = InformedSample(c_best, c_min, x_center, C, map)

        # get nearest node
        new_node = SearchNode(random_position)
        nearest_position = tree.nearest_position(new_node.position)
        nearest_node = expanded_nodes[(nearest_position[0], nearest_position[1])]

        distance = dist(new_node.position, nearest_node.position)
        new_node.distance = distance + nearest_node.distance

        # check if new_node is within step distance from nearest_node
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
            continue

        # Assign parent based on lowest distance among neighborhood points
        new_node.parent = nearest_node
        # surrounding_positions = naive_surrounding_positions(new_node.position, neighborhood, expanded_nodes)
        surrounding_positions = tree.surrounding_positions(new_node.position, neighborhood)
        for position in surrounding_positions:
            node = expanded_nodes[(position[0], position[1])]
            neighbor_distance = dist(new_node.position, node.position)
            if node.distance + neighbor_distance < new_node.distance:
                if not in_line_collision([node.position, new_node.position], map):
                    new_node.parent = node
                    new_node.distance = node.distance + neighbor_distance

        # Rewire surrounding nodes to new_node if feasible
        for position in surrounding_positions:
            node = expanded_nodes[(position[0], position[1])]
            neighbor_distance = dist(new_node.position, node.position)
            if new_node.distance + neighbor_distance < node.distance:
                if not in_line_collision([node.position, new_node.position], map):
                    node.parent = new_node
                    node.distance = new_node.distance + neighbor_distance
        

        # check if new_node is within goal boundary
        dist_to_goal = dist(new_node.position, goal)
        total_distance = new_node.distance + dist_to_goal
        if dist_to_goal <= goal_radius and total_distance < goal_node.distance:
            c_best = total_distance
            goal_node.parent = new_node
            goal_node.distance = total_distance
            found = True

        # add new node to graph and tree
        expanded_nodes[(new_node.position[0], new_node.position[1])] = new_node
        tree.add(new_node.position)
        num_expanded = num_expanded + 1

    if (found):
        print(f"Path from {start} to {goal} found with distance {goal_node.distance} after expanding {num_expanded} nodes")
        node = goal_node
        while (node.parent != None):
            path.append(node.position)
            node = node.parent
        
        path.append(start)

        path.reverse()

    return path, num_expanded, expanded_nodes




