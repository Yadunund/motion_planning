#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from OccupancyMap import OccupancyMap2D


def get_grid(map):
    n_rows = len(map.map)
    n_cols = int(np.size(map.map)/n_rows)
    fig, ax = plt.subplots(1, 2, tight_layout=True)

    for i in range(n_rows + 1):
        for j in range(len(ax)):
            ax[j].axhline(i, lw = 1, color = 'k', zorder = 5)

    for i in range(n_cols + 1):
        for j in range(len(ax)):
            ax[j].axvline(i, lw = 1, color = 'k', zorder = 5)

    for i in range(len(ax)):
        ax[i].axis('on')
        
    return fig, ax
    
def display_solution(path, solver_steps, map, start, goal):
    map_solver = copy.deepcopy(map)
    n_rows = len(map.map)
    n_cols = int(np.size(map.map)/n_rows)
    fig, ax = get_grid(map)

    # Visualizing path
    # set 0 to white, 1 to black, 2(start) to yellow, 3(goal) red and 4(path) to green
    cmap = matplotlib.colors.ListedColormap(['w', 'k', 'y', 'r', 'g'])
    map.map[start[0]][start[1]] = 2
    map.map[goal[0]][goal[1]] = 3
    for i in range(1, len(path) - 1):
        map.map[path[i][0]][path[i][1]] = 4
    ax[0].imshow(map.map, interpolation = 'none', cmap = cmap, extent = [0, n_rows, 0, n_cols], zorder = 0)

    # Visualizing solver
    ani = FuncAnimation(fig, animate, frames = solver_steps, fargs = [map_solver, ax[1]], repeat= True, interval = 100)
    plt.show()

def animate(step, map, ax):
    map.display_map()
    cmap = matplotlib.colors.ListedColormap(['w', 'k', 'r'])
    n = len(map.map)
    index = None
    visited = None
    for item in step.items():
        index = item[0]
        visited = item[1]
    for v in visited:
        map.map[v[0]][v[1]] = 2
    
    # node under expansion
    # map.map[index[0]][index[1]] = 3
    ax.imshow(map.map, interpolation = 'none', cmap = cmap, extent = [0, n, 0, n], zorder = 0)

        
def animate_solver(solver_steps, map):
    return
    # fig, ax = get_grid(map)
    # plt.show()
    # 