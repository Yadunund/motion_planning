from point import Point

class Polygon:
    def __init__(self, points):
        self.points = points
        #  self.edge_constants = self.compute_edge_constants()

    def points(self):
        return self.points
    def add_point(self, point):
        self.points.append(point)
        return self.points
    def size(self):
        return len(self.points)
    # def compute_edge_constants(self):
    #     edge_constants = []
    #     for i in range(self.size()):
    #         edges