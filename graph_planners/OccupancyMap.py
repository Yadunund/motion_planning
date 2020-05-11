#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

class OccupancyMap2D:
    def __init__(self, n, obstacles = []):
        self.map = np.zeros((n,n), int)
        for obstacle in obstacles:
            assert(len(obstacle) == 2)
            self.map[obstacle[0]][obstacle[1]] = 1.0
        self.display_map()
        
    def display_map(self):
        print('Map:')
        for row in self.map:
            print(f'    {row}')
        
    
    