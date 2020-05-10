#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 10 21:49:15 2020

@author: yadu
"""

import sys
import argparse
import numpy as np

from OccupancyMap import OccupancyMap2D

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument()
    n = 10
    obstacles = []
    start = [int(n/2), 0]
    goal = [int(n/2), int(n - 1)]
    
    # create a wall down the middle of the map except for bottom-most row
    for i in range(n-1):
        obstacles.append([i, int(n/2)])
        
    map = OccupancyMap2D(n, obstacles)


if __name__ == '__main__':
    main()