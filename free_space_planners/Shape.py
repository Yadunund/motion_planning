class ConvexShape:
    ''' We assume the points supplied here are consecutive boundary points'''
    def __init__(self, points:[[]]):
        assert len(points) > 2, "A shape requires at least three points"
        self.points = points
        assert self.__is_convex(), "Boundary points supplied do not form a convex shape"

    def __is_convex(self):
        cross_products = []
        for i in range(self.size()):
            j = i + 1
            if j > self.size() - 1:
                j = j % self.size()
            k = i + 2
            if k > self.size() -1:
                k = k % self.size()
            dx1 = self.points[j][0] - self.points[i][0]
            dy1 = self.points[j][1] - self.points[i][1]
            dx2 = self.points[k][0] - self.points[j][0]
            dy2 = self.points[k][1] - self.points[j][1]
            zcrossproduct = dx1*dy2 - dy1*dx2
            cross_products.append(zcrossproduct)
        previous_sign = cross_products[0] > 0
        for i in range(1, len(cross_products)):
            sign = cross_products[i] > 0
            if sign != previous_sign:
                return False
            previous_sign = sign
        
        return True

    def size(self):
        return len(self.points)


#          given p[k], p[k+1], p[k+2] each with coordinates x, y:
