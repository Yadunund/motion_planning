#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import numpy as np
from Node import Node
from OccupancyMap import OccupancyMap2D

# return [path, number of expanded nodes, solver_steps]
def DijkstraSolver(map, start, goal, performance = False):
    path = []   
    n_rows = map.n_rows
    n_cols = map.n_cols
    # check if start and goal are valid
    assert(map.is_valid(start))
    assert(map.is_valid(goal))
    
    # map index tuple to Node
    node_queue = []
    expanded_nodes = {}
    solver_steps = []
    found = False
    
    # each node stores distance and parent
    # expand based on lowest distance in node_queue
    start_node = Node(start, 0)
    node_queue.append(start_node)
    
    print(f'Solving using Dijkstras...')
    while (node_queue and not found):
        # get node with smallest distance
        min_index = 0
        min_dist = np.inf
        for i in range(len(node_queue)):
            if node_queue[i].distance < min_dist:
                min_dist = node_queue[i].distance
                min_index = i 
        node = node_queue.pop(min_index)

        # print(f'    Expanding node {node.index} with distance {node.distance}')
        # todo cache neighbors
        neighbors = map.get_neighbors(node.index)
        # solver_steps.append({node.index:neighbors})
        # print(f'node {node.index}: {neighbors}')
        for neighbor in neighbors:
            # print(f'        found neighbor {neighbor}')
            if neighbor == goal:
                found = True
                expanded_nodes[neighbor] = Node(neighbor, node.distance + 1, node)
                break
            
            if neighbor in expanded_nodes:
                # print(f'            previously visited {expanded_nodes[neighbor].index}')
                # we do not expect this to happen with the grid map
                if expanded_nodes[neighbor].distance > node.distance + 1:
                    expanded_nodes[neighbor].distance = node.distance + 1
                    expanded_nodes[neighbor].parent = node
            else:
                if neighbor not in [n.index for n in node_queue]:
                    node_queue.append(Node(neighbor, node.distance + 1, node))
                    # print(f'            appending unvisited {neighbor} with distance {node.distance + 1}')

        expanded_nodes[node.index] = node
        if not performance:
            solver_steps.append({node.index:copy.deepcopy(expanded_nodes)})

    # once we are done exploring, we check if path was found
    if goal in expanded_nodes:
        print(f'    Found goal {goal} with distance {expanded_nodes[goal].distance}')
        node = expanded_nodes[goal]
        while (node.index != start):
            path.append(node.index)
            node = node.parent        
    
        path.append(start_node.index)
        
    path.reverse()
    num_expanded = len(expanded_nodes) -1
    
    return path, num_expanded, solver_steps