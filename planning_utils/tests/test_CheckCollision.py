#!/usr/bin/env python3

from motion_planning.planning_utils.CheckCollision import CheckCollision
from ..polygon import Polygon
from ..point import Point

def main():
    p = Point(5, 5)
    triangle = Polygon([Point(0,0), Point(10,10), Point(5,10)])
    collision = CheckCollision(triangle, p)
    print(f"Collision: {collision}")

if __name__ == "__main__":
    main()