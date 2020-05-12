import numpy as np
from OccupancyMap import OccupancyMap2D

class Node:
    def __init__(self, index, distance = np.inf, parent = None, f = np.inf):
        self.index = index
        self.distance = distance            
        self.parent = parent
        self.f = f

