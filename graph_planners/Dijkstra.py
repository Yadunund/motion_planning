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
def DijkstraSolver(occupancy_map, start, goal):
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
    node_queue = []
    visited_nodes = {}
    solver_steps = []
    found = False
    
    # each node stores distance and parent
    # expand based on lowest distance in node_queue
    start_node = Node(start, 0)
    node_queue.append(start_node)
    
    print(f'Solving using Dijkstras...')
    while (node_queue and not found):
        print(f'Unexpanded nodes: {[x.index for x in node_queue]}')
        # get node with smallest distance
        min_index = 0
        min_dist = np.inf
        for i in range(len(node_queue)):
            if node_queue[i].distance < min_dist:
                min_dist = node_queue[i].distance
                min_index = i 
        node = node_queue.pop(min_index)
        

        print(f'    Expanding node {node.index} with distance {node.distance}')
        visited_nodes[node.index] = node
        # solver_steps.append({node.index:[x for x in visited_nodes.keys()]})
        # todo cache neighbors
        neighbors = get_neighbors(node.index, map)
        solver_steps.append({node.index:neighbors})
        print(f'node {node.index}: {neighbors}')
        for neighbor in neighbors:
            print(f'        found neighbor {neighbor}')
            if neighbor == goal:
                found = True
                visited_nodes[neighbor] = Node(neighbor, node.distance + 1, node)
                break
            
            if neighbor in visited_nodes:
                print(f'            previously visited {visited_nodes[neighbor].index}')
                # we do not expect this to happen with the grid map
                if visited_nodes[neighbor].distance > node.distance + 1:
                    visited_nodes[neighbor].distance = node.distance + 1
                    visited_nodes[neighbor].parent = node
            else:
                if neighbor not in [n.index for n in node_queue]:
                    node_queue.append(Node(neighbor, node.distance + 1, node))
                    print(f'            appending unvisited {neighbor} with distance {node.distance + 1}')

    
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
    
    return path, num_expanded, solver_steps