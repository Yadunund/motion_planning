from Shape import ConvexShape

class Obstacle:
    def __init__(self, shape:ConvexShape):
        # We only support triangular obstacles
        assert(shape.size() == 3)
        self.shape = shape
        self.triangles = self.__decompose_triangles()


    def __decompose_triangles(self):
        triangles = []
        if self.shape.size() == 3:
            triangles.append(ConvexShape(self.shape.points))
            return triangles

        return triangles