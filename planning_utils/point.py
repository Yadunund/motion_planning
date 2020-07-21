import numpy as np

class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    def X(self):
        return self.x
    def X(self, x):
        self.x = x
        return self.x
    def Y(self):
        return self.y
    def Y(self, y):
        self.y = y
        return self.y
    def Z(self):
        return self.z
    def Z(self, z):
        self.z = z
        return self.z
    

  