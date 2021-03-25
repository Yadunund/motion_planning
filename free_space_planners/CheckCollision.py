from point import Point
from polygon import Polygon

def CheckCollision(triangle, p):
    assert(triangle.size() == 3)

    # we use half plane method to determine if point lies inside the triangle
    points = triangle.points
    v1 = points[0]
    v2 = points[1]
    v3 = points[2]

    w1 = (v1.x*(v3.y-v1.y)+(p.y-v1.y)*(v3.x-v1.x)-p.x*(v3.x-v1.y))/((v2.y-v1.y)*(v3.x-v1.x)-(v2.x-v1.x)*(v3.y-v1.y))
    w2 = (p.y-v1.y-w1*(v2.y-v1.y))/(v3.y-v1.y)
    print(f"w1:{w1} w2:{w2}")
    if w1 < 0:
        return False
    elif w2 < 0:
        return False
    elif w1+w2>1:
        return False
    else:
        return True

