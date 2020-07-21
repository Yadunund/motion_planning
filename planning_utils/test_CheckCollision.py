#!/usr/bin/env python3

from point import Point
from polygon import Polygon
from CheckCollision import CheckCollision

def main():
    p = Point(0, 0)
    v1 = Point(-1,-1)
    v2 = Point(1,-1)
    v3 = Point(0,1)
    triangle = Polygon([v1,v2,v3])
    collision = CheckCollision(triangle, p)
    print(f"Collision: {collision}")

if __name__ == "__main__":
    main()