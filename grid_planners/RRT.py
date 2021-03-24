#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from Node import Node
from OccupancyMap import OccupancyMap2D

def H(start, goal):
  return np.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

def get_nearest_node(node:Node, sampled_nodes:list):
    min_dist = np.inf
    nearest_node = None
    for n in sampled_nodes:
        dist = H(n.index, node.index)
        if dist <= min_dist:
            min_dist = dist
            nearest_node = n
    assert(nearest_node is not None)
    return (nearest_node, min_dist)

# return [path, number of expanded nodes, solver_steps]
def RRTSolver(map, start, goal, performance=False):
    path = []   
    n_rows = map.n_rows
    n_cols = map.n_cols
    # check if start and goal are valid
    assert(map.is_valid(start))
    assert(map.is_valid(goal))
    
    solver_steps = []

    n = 0 # number of iterations
    max_step = 1.414
    sampled_nodes = []
    # flag if solution is found
    found = False

    goal_node = Node(goal, 0, None)
    start_node = Node(start, 0, None)
    sampled_nodes.append(start_node)

    while (not found):
        n = n + 1
        random_index = map.random_sample()
        # Check if collision
        if map.map[random_index[0]][random_index[1]] == 1:
            continue

        # New node
        node = Node(random_index, 0, None)
        # Get nearest node in sampled nodes
        nearest_node, dist = get_nearest_node(node, sampled_nodes)
        node.parent = nearest_node

        # Find the neighbor of nearest_node along direction of node
        neighbors = map.get_neighbors(nearest_node.index)
        projection = -np.inf
        selected_index = None
        selected_cost = 0
        b = np.array([node.index[0] - nearest_node.index[0], node.index[1] - nearest_node.index[1]])
        for neighbor in neighbors:
            i = neighbor[0]
            a = np.array([i[0]-nearest_node.index[0],i[1]-nearest_node.index[1]])
            dot = np.dot(a, b)
            if (dot > projection):
                projection = dot
                selected_index = i
                selected_cost = neighbor[1]
        assert(selected_index)
        if selected_index == goal:
            found = True
            goal_node.parent = nearest_node
            goal_node.distance = nearest_node.distance + selected_cost
            continue
        node.index = selected_index
        node.distance = nearest_node.distance + selected_cost
        sampled_nodes.append(node)

    print(f"Found goal node after {n} expansions with distance {goal_node.distance}")
    node = goal_node
    while (node.parent is not None):
        path.append(node.index)
        node = node.parent
    
    path.append(start)
    path.reverse()

        
    
    return path, n, solver_steps
