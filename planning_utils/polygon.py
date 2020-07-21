import Point

class Polygon:
    self.points = []
    def __init__(self, points):
        self.points = points
    
    def points(self):
        return points
    def add_point(self, point):
        self.points.append(point)
        return self.points
    def size(self):
        return len(self.points)