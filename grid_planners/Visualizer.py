#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from OccupancyMap import OccupancyMap2D


def get_grid(map):
    n_rows = map.n_rows
    n_cols = map.n_cols
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
    map_copy = copy.deepcopy(map)
    n_rows = map.n_rows
    n_cols = map.n_cols
    fig, ax = get_grid(map)

    # Visualizing path
    # set 0 to white, 1 to black, 2(start) to yellow, 3(goal) red and 4(path) to green
    cmap = matplotlib.colors.ListedColormap(['w', 'k', 'y', 'r', 'g'])
    map_copy.map[start[0]][start[1]] = 2
    map_copy.map[goal[0]][goal[1]] = 3
    for i in range(1, len(path) - 1):
        map_copy.map[path[i][0]][path[i][1]] = 4
    ax[0].imshow(map_copy.map, interpolation = 'none', cmap = cmap, extent = [0, n_rows, 0, n_cols], zorder = 0)

    # Visualizing solver
    ani = FuncAnimation(fig, animate, frames = solver_steps[:len(solver_steps) - 1], fargs = [map, ax[1]], repeat= True, interval = 100)
    plt.show()

def animate(step, map, ax):
    # map_copy = copy.deepcopy(map)
    map_copy = map
    cmap = matplotlib.colors.ListedColormap(['w', 'k', 'r'])
    index = None
    visited = None
    for item in step.items():
        index = item[0]
        visited = item[1]
    for v in visited:
        map_copy.map[v[0]][v[1]] = 2
    
    # node under expansion
    # map.map[index[0]][index[1]] = 3
    ax.imshow(map_copy.map, interpolation = 'none', cmap = cmap, extent = [0, map.n_rows, 0, map.n_cols], zorder = 0)

        
def animate_solver(solver_steps, map):
    return
    # fig, ax = get_grid(map)
    # plt.show()
    # 