#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from Node import Node
from OccupancyMap import OccupancyMap2D

def H(start, goal):
  return np.sqrt((goal[0] - start[0])**2 + (goal[1] - start[1])**2)

# return [path, number of expanded nodes, solver_steps]
def AStarSolver(map, start, goal):
    path = []   
    n_rows = map.n_rows
    n_cols = map.n_cols
    # check if start and goal are valid
    assert(map.is_valid(start))
    assert(map.is_valid(goal))
    
    # Nodes to be processed by solver
    node_queue = {}
    # Nodes discovered by solver
    nodes = {}
    # Node indices expanded by solver
    expanded_nodes = []
    # used for visualization
    solver_steps = []
    # flag if solution is found
    found = False
    
    # each node stores distance and parent
    start_node = Node(start, 0, None, H(start, goal))
    node_queue[start_node.index] = start_node
    nodes[start_node.index] = start_node
    
    print(f'Solving using A*...')
    while (node_queue and not found):
        # pop node with smallest f-value
        min_index = start
        min_value = np.inf
        for i in node_queue.keys():
          if node_queue[i].f < min_value:
            min_value = node_queue[i].f
            min_index = i
        
        node = node_queue.pop(min_index)
        # print(f'    Expanding node {node.index} with f-value {node.f}')
        neighbors = map.get_neighbors(node.index)
        solver_steps.append({node.index:neighbors})

        for neighbor in neighbors:
            if neighbor == goal:
                found = True
                nodes[goal] = Node(goal, node.distance + 1, node, H(neighbor, goal))
                break
            if neighbor in nodes.keys():
                if nodes[neighbor].distance > node.distance + 1:
                    nodes[neighbor].distance = node.distance + 1
                    nodes[neighbor].f = node.distance + 1 + H(neighbor, goal)
                    nodes[neighbor].parent = node
                    node_queue[neighbor] = nodes[neighbor]
            else:
                neighbor_node = Node(neighbor,
                    node.distance + 1,
                    node,
                    node.distance + 1 + H(neighbor, goal))
                node_queue[neighbor] = neighbor_node
                nodes[neighbor] = neighbor_node

        expanded_nodes.append(node.index)

    
    if found:
      node = nodes[goal]
      print(f'    Found goal {goal} with distance {node.distance} and f {node.f}')
      while (node.index != start):
            path.append(node.index)
            node = node.parent        
    
      path.append(start_node.index)

    path.reverse()
    num_expanded = len(expanded_nodes)
    
    return path, num_expanded, solver_steps
