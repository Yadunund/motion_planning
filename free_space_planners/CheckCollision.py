from Shape import ConvexShape

class BoundingBox:
    def __init__(self, min:list, max:list):
        self.x_min = min[0]
        self.y_min = min[1]
        self.x_max = max[0]
        self.y_max = max[1]

def get_bounding_box(points:list):
    x = []
    y = []
    for p in points:
        x.append(p[0])
        y.append(p[1])
    return BoundingBox([min(x), min(y)], [max(x), max(y)])

def BroadPhaseAABB(box1:BoundingBox, box2:BoundingBox):

    if box1.x_max < box2.x_min:
        return False
    if box2.x_max < box1.x_min:
        return False
    if box1.y_max < box2.y_min:
        return False
    if box2.y_max < box1.y_min:
        return False

    return True

def sign (p1, p2, p3):
    # Cross product of (p1 - p3) x (p2 - p3)
    return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

def orientation(p1, p2, p3):
    # based on the value of sign(), assign an orientation to the point p1 wrt line p2p3
    s = sign(p1, p2 , p3)
    if s == 0:
        return 0 # colinear
    elif s < 0:
        return 1 # counterclockwise
    else:
        return 2 # clockwise


def colinear(p1, p2, p3):
    ''' Check if p1 lies on line segment p2p3'''
    return (p1[0] <= max(p2[0], p3[0])) and (p1[0] >= min(p2[0], p3[0]))\
         and (p1[1] <= max(p2[1], p3[1])) and (p1[1] > min(p2[1], p3[1]))


def LineLineCollision(l1:list, l2:list):
    assert(len(l1) > 1 and len(l1[0]) > 1)
    assert(len(l2) > 1 and len(l2[0]) > 1)

    p1 = l1[0]
    q1 = l1[1]
    p2 = l2[0]
    q2 = l2[1]

    o1 = orientation(p2, p1, q1)
    o2 = orientation(q2, p1, q1)
    if (o1 == o2):
        return False
    o3 = orientation(p1, p2, q2)
    o4 = orientation(p2, p2, q2)
    if (o3 == o4):
        return False
  
    if (o1 != o2 and o3 != o4):
        return True
    
    # Colinear cases
    # if (o1 == 0 and colinear(p2, p1, q1)):
    #     return True
    # if (o2 == 0 and colinear(q2, p1, q1)):
    #     return True
    # if (o3 == 0 and colinear(p1, p2, q2)):
    #     return True
    # if (o4 == 0 and colinear(q1, p2, q2)):
    #     return True
    return False

def TrainglePointCollision(triangle:ConvexShape, p:list):
    assert(triangle.size() == 3)
    assert(len(p) > 1)

    box = get_bounding_box(triangle.points)
    x, y = p
    broad_phase = (x > box.x_min and x < box.x_max) and (y > box.y_min and y < box.y_max)
    if not broad_phase:
        return False

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

def TriangleLineCollision(triangle:ConvexShape, l:list):
    assert(triangle.size() == 3)
    assert(len(l) > 1 and len(l[0]) > 1)

    box1 = get_bounding_box(triangle.points)
    box2 = get_bounding_box(l)

    if not BroadPhaseAABB(box1, box2):
        return False

    v1 = triangle.points[0]
    v2 = triangle.points[1]
    v3 = triangle.points[2]

    # We check for line segment collision between pairs of triangle edges and the given line
    c1 = LineLineCollision([v1, v2], l)
    if c1:
        return True
    c2 = LineLineCollision([v2, v3], l)
    if c2:
        return True
    c3 = LineLineCollision([v3, v1], l)
    if c3:
        return True
    return False