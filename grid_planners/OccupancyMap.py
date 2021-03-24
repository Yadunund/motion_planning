#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from random import randrange

class OccupancyMap2D:
    def __init__(self, n_rows, n_cols = None, obstacles = []):
        #todo support 
        self.n_rows = n_rows
        if n_cols is not None:
          self.n_cols = n_cols
        else:
          n_cols = self.n_rows

        self.map = np.zeros((self.n_rows,self.n_cols), int)
        for obstacle in obstacles:
            assert(len(obstacle) == 2)
            self.map[obstacle[0]][obstacle[1]] = 1.0
                    
    def display_map(self):
        print('Map:')
        for row in self.map:
            print(f'    {row}')
        
    ''' Returns a tuple of index and cost ((x,y), c) '''
    def get_neighbors(self, index):
        neighbors = []
        # up
        i = index[0] - 1
        j = index[1]
        if i >= 0 and self.map[i][j] == 0:
            neighbors.append(((i, j), 1))
        # down
        i = index[0] + 1
        if i < self.n_rows and self.map[i][j] == 0:
            neighbors.append(((i, j), 1))
        # left
        i = index[0]
        j = index[1] - 1
        if j >= 0 and self.map[i][j] == 0:
            neighbors.append(((i, j), 1))
        # right
        j = index[1] + 1
        if j < self.n_cols and self.map[i][j] == 0:
            neighbors.append(((i, j), 1))
        # NE
        i = index[0] - 1
        j = index[1] + 1
        if i >= 0 and j < self.n_cols and self.map[i][j] == 0:
            neighbors.append(((i, j), 1.414))
        # SE
        i = index[0] + 1
        j = index[1] + 1
        if i < self.n_rows and j < self.n_cols and self.map[i][j] == 0:
            neighbors.append(((i, j), 1.414))
        # SW
        i = index[0] + 1
        j = index[1] - 1
        if i < self.n_rows and j >= 0 and self.map[i][j] == 0:
            neighbors.append(((i, j), 1.414))
        # NW
        i = index[0] - 1
        j = index[1] - 1
        if i >= 0 and j >=0 and self.map[i][j] == 0:
            neighbors.append(((i, j), 1.414))
        
        return neighbors
    
    def is_valid(self, index):
      return index[0] < self.n_rows and index[1] < self.n_cols
    
    def random_sample(self):
        x = randrange(self.n_rows)
        y = randrange(self.n_cols)
        return (x, y)
    