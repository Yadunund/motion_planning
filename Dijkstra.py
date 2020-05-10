#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 23:31:24 2020

@author: yadu
"""

import numpy as np

class Node:
    def __init__(self, index, distance = None, parent = None):
        self.index = index
        self.distance = np.inf
        if distance:
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
def DijkstraSolver(occupancy_map, start, goal):
    path = []
    node_list = []
    map = occupancy_map.map
    
    n_rows = len(map)
    n_cols = np.size(map)/n_rows
    # check if start and goal are valid
    assert(start[0] < n_rows)
    assert(start[1] < n_cols)
    assert(goal[0] < n_rows)
    assert(goal[1] < n_cols)
    
    # each node stores distance and parent
    # expand based on lowest distance in node_list
    start_node = Node(start, 0)
    node_list.append(start_node)
    
    # map index tuple to Node
    visited_nodes = {}
    found = False
    
    print(f'Solving using Dijkstras...')
    while (node_list and not found):
        # we have not implemented any priority at this point
        node = node_list.pop()
        print(f'    Expanding node {node.index}')
        visited_nodes[node.index] = node
        # todo cache neighbors
        for neighbor in get_neighbors(node.index, map):
            if neighbor == goal:
                found = True
                visited_nodes[neighbor] = Node(neighbor, node.distance + 1, node)
                break
            elif neighbor in visited_nodes:
                if visited_nodes[neighbor].distance < node.distance - 1:
                    # visited_nodes[neighbor].distance = node.distance + 1
                    # visited_nodes[neighbor].parent = node.index
                    visited_nodes[node.index] = Node(node.index, visited_nodes[neighbor].distance + 1, visited_nodes[neighbor])
                    print(f'    Found previously visited node {visited_nodes[neighbor]}')
                    print(f'        Updating distance to {visited_nodes[neighbor].distance}')
            else:
                node_list.append(Node(neighbor, node.distance + 1, node))
                                 
    print(f'    Visited {len(visited_nodes)}')
    # once we are done exploring, we check if path was found
    if goal in visited_nodes:
        print(f'        Found goal {goal} in visited_nodes')
        node = visited_nodes[goal]
        while (node.index != start):
            path.append(node.index)
            node = node.parent        
    
        path.append(start_node.index)
        
    path.reverse()
    num_expanded = len(visited_nodes) -1
    
    return path, num_expanded