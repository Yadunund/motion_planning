import numpy as np 

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Map import Map
from Obstacle import Obstacle

def display_solution(map:Map, start:list, goal:list, path:list, expanded_nodes:list, parent=''):
    fig = plt.figure(figsize=(10,10), dpi=100)
    plt.xlim([0, map.width])
    plt.ylim([0, map.height])
    for obstacle in map.obstacles:
        polygon = plt.Polygon(obstacle.shape.points, True)
        plt.gca().add_line(polygon)

    # plot the expansion
    for node in expanded_nodes:
        plt.plot([node.position[0]], [node.position[1]], 'ro')
        if node.parent is not None:
            edge = [node.position, node.parent.position]
            line = plt.Polygon(edge, closed=None, fill=None, edgecolor='r')
            plt.gca().add_line(line)

    if path:
      line = plt.Polygon(path, closed=None, fill=None, edgecolor='k', linewidth = 5.0)
      plt.gca().add_line(line)

    plt.plot([start[0]], [start[1]], 'yo') # start
    plt.plot([goal[0]], [goal[1]], 'go')

    plt.show()


    
