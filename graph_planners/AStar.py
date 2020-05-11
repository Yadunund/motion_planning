#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class Node:
    def __init__(self, index, distance = None, parent = None):
        self.index = index
        self.distance = distance            
        self.parent = parent


def get_neighbors(index, map):
    n_rows = len(map)
    n_cols = np.size(map)/n_rows
    neighbors = []
    # up
    i = index[0] - 1
    j = index[1]
    if i >= 0 and map[i][j] == 0:
        neighbors.append((i, j))
    # down
    i = index[0] + 1
    if i < n_rows and map[i][j] == 0:
        neighbors.append((i, j))
    # left
    i = index[0]
    j = index[1] - 1
    if j >= 0 and map[i][j] == 0:
        neighbors.append((i, j))
    # right
    j = index[1] + 1
    if j < n_cols and map[i][j] == 0:
        neighbors.append((i, j))
    
    return neighbors


# return [path, number of expanded nodes]
def AStarSolver(occupancy_map, start, goal):
    path = []
    map = occupancy_map.map
    
    n_rows = len(map)
    n_cols = np.size(map)/n_rows
    # check if start and goal are valid
    assert(start[0] < n_rows)
    assert(start[1] < n_cols)
    assert(goal[0] < n_rows)
    assert(goal[1] < n_cols)
    
    # map index tuple to Node
    unvisited_nodes = []
    visited_nodes = {}
    found = False
    
    # each node stores distance and parent
    # expand based on lowest distance in unvisited_nodes
    start_node = Node(start, 0)
    unvisited_nodes.append(start_node)
    
    print(f'Solving using A*...')
    while (unvisited_nodes and not found):
        continue
        
    path.reverse()
    num_expanded = len(visited_nodes) -1
    
    return path, num_expanded