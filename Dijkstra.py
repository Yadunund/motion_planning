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
        print(f'Unexpanded nodes: {[x.index for x in node_list]}')
        # get node with smallest distance
        
        min_index = 0
        min_dist = np.inf
        for i in range(len(node_list)):
            if node_list[i].distance < min_dist:
                min_dist = node_list[i].distance
                min_index = i 
        node = node_list.pop(min_index)
        

        print(f'    Expanding node {node.index} with distance {node.distance}')
        visited_nodes[node.index] = node
        # todo cache neighbors
        for neighbor in get_neighbors(node.index, map):
            print(f'        found neighbor {neighbor}')
            if neighbor == goal:
                found = True
                visited_nodes[neighbor] = Node(neighbor, node.distance + 1, node)
                break
            
            if neighbor in visited_nodes:
                print(f'            previously visited {visited_nodes[neighbor].index}')
                if visited_nodes[neighbor].distance > node.distance + 1:
                    visited_nodes[neighbor].distance = node.distance + 1
                    visited_nodes[neighbor].parent = node
                    # visited_nodes[node.index] = Node(node.index, neighbor_node.distance + 1, neighbor_node)
            else:
                if neighbor not in [n.index for n in node_list]:
                    node_list.append(Node(neighbor, node.distance + 1, node))
                    print(f'            appending unvisited {neighbor} with distance {node.distance + 1}')
                                 
    print(f'    Visited {len(visited_nodes)}')
    
    # once we are done exploring, we check if path was found
    if goal in visited_nodes:
        print(f'        Found goal {goal} with distance {visited_nodes[goal].distance}')
        node = visited_nodes[goal]
        while (node.index != start):
            path.append(node.index)
            node = node.parent        
    
        path.append(start_node.index)
        
    path.reverse()
    num_expanded = len(visited_nodes) -1
    
    return path, num_expanded