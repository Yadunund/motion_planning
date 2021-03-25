import numpy as np
import random

class Map:
    def __init__(self, width, height, obstacles:list):
        self.width = width
        self.height = height
        self.obstacles = obstacles
    
    def is_valid_position(self, position:list):
        return position[0] <= self.width and position[1] <= self.height
    
    def random_position(self):
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return [x,y]