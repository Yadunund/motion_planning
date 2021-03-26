from Shape import ConvexShape

def sign (p1, p2, p3):
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def TrainglePointCollision(triangle:ConvexShape, p:[]):
    assert(triangle.size() == 3)
    # we use half plane method to determine if point lies inside the triangle
    # https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
    points = triangle.points
    v1 = points[0]
    v2 = points[1]
    v3 = points[2]
    # print(f"Checking collition of {p} with triangle of vertices {v1}, {v2}, {v3}")

    d1 = sign(p, v1, v2)
    d2 = sign(p, v2, v3)
    d3 = sign(p, v3, v1)

    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    return not (has_neg and has_pos)
