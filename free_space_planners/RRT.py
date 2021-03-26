from KdTree import KdTree
from Node import SearchNode
from Map import Map

from CheckCollision import TrainglePointCollision

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import math
import threading
import time


def in_collision(position, map:Map):
    for obstacle in map.obstacles:
        for triangle in obstacle.triangles:
            collision = TrainglePointCollision(triangle, position)
            if collision == True:
                return True
    return False

def dist(a:list, b:list):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def RRTSolver(map:Map, start:list, goal:list, steps=False):
    goal_radius = 0.5 # meters
    max_step = 1.0
  
    if in_collision(start, map):
        print(f"[error] start {start} is on an obstacle")
        return
    if in_collision(goal, map):
        print(f"[error] goal {goal} is on an obstacle")
        return

    if dist(start, goal) <= goal_radius:
        print(f"Start is already within goal radius")
        return
    
    path = []
    num_expanded = 0
    expanded_nodes = {}

    root = SearchNode(start)
    expanded_nodes[(root.position[0], root.position[1])] = root
    tree = KdTree(start)

    goal_node = None
    found = False
    while (not found):
        num_expanded = num_expanded + 1
        random_position = map.random_position()
        new_node = SearchNode(random_position)
        # print(f"Random new node generated with position {new_node.position}")
        if (in_collision(new_node.position, map)):
            continue
        # get nearest node
        nearest_position = tree.nearest_position(new_node.position)
        nearest_node = expanded_nodes[(nearest_position[0], nearest_position[1])]
        # print(f"Found nearest node with position {nearest_node.position}")
        # check if new_node is within step distance from nearest_node
        distance = dist(new_node.position, nearest_node.position)
        new_node.distance = distance + nearest_node.distance
        if distance > max_step:
            x1, y1 = nearest_node.position
            x2, y2 = new_node.position
            v = [x2 - x1, y2 - y1]
            magnitude_v = math.sqrt(v[0]**2 + v[1]**2)
            u = [v[0]/magnitude_v, v[1]/magnitude_v]
            new_point = [x1 + max_step*u[0], y1 + max_step*u[1]]
            new_dist = dist(new_point, nearest_node.position)
            # print(f"new_dist: {new_dist}")
            # assert( new_dist <= max_step)
            new_node.position = new_point
            new_node.distance = new_dist + nearest_node.distance
            # print(f"nearest_node.distance: {nearest_node.distance}")
            # print(f"    Position of new node corrected to {new_node.position} with distance {new_dist}")
        if (in_collision(new_node.position, map)):
            continue
        # print(f" new_node is {new_node.distance} away from start")
        new_node.parent = nearest_node
        expanded_nodes[(new_node.position[0], new_node.position[1])] = new_node

        # check if new_node is within goal boundary
        dist_to_goal = dist(new_node.position, goal)
        if dist_to_goal <= goal_radius:
            goal_node = new_node
            goal_node.distance = goal_node.distance + dist_to_goal
            found = True

        # add new node to tree
        tree.add(new_node.position)
        # print(f"num_expanded: {num_expanded}")

    if (goal_node):
        print(f"Path from {start} to {goal} found with distance {goal_node.distance} after expanding {num_expanded} nodes")
        node = goal_node
        while (node.parent != None):
            path.append(node.position)
            node = node.parent
        
        path.append(start)

        path.reverse()

    return path, num_expanded, expanded_nodes




