from Visualizer import *
from Map import Map
from Shape import ConvexShape
from Obstacle import Obstacle


points = [[10, 60], [60, 70], [70, 60]]
shape = ConvexShape(points)
obstacle = Obstacle(shape)
map = Map(100, 100, [obstacle])

display_solution(map, [0,0], [100,0], [])