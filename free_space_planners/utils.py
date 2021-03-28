from Map import Map
from Shape import ConvexShape
from CheckCollision import TrainglePointCollision, TriangleLineCollision
import math

def dist(a:list, b:list):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def in_point_collision(position:list, map:Map):
    for obstacle in map.obstacles:
        for triangle in obstacle.triangles:
            collision = TrainglePointCollision(triangle, position)
            if collision == True:
                return True
    return False

def in_line_collision(line:list, map:Map):
    for obstacle in map.obstacles:
        for triangle in obstacle.triangles:
            collision = TriangleLineCollision(triangle, line)
            if collision == True:
                return True
    return False
