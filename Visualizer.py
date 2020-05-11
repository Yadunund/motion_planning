#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from OccupancyMap import OccupancyMap2D


def display_solution(path, map, start, goal):
    n_rows = len(map.map)
    n_cols = int(np.size(map.map)/n_rows)
    fig, ax = plt.subplots(1, 1, tight_layout=True)
    # set 0 to white, 1 to black, 2(start) to yellow, 3(goal) red and 4(path) to green
    cmap = matplotlib.colors.ListedColormap(['w', 'k', 'y', 'r', 'g'])
    map.map[start[0]][start[1]] = 2
    map.map[goal[0]][goal[1]] = 3
    
    for i in range(1, len(path) - 1):
        map.map[path[i][0]][path[i][1]] = 4

    for i in range(n_rows + 1):
        ax.axhline(i, lw = 1, color = 'k', zorder = 5)
    for i in range(n_cols + 1):
        ax.axvline(i, lw = 1, color = 'k', zorder = 5)
    ax.imshow(map.map, interpolation = 'none', cmap = cmap, extent = [0, n_rows, 0, n_cols], zorder = 0)
    ax.axis('on')
    plt.show()