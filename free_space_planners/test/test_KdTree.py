#! /usr/var/env python3

import os, sys
sys.path.insert(0, os.path.abspath(".."))

from KdTree import KdTree
from Node import SearchNode

def main():
    r = SearchNode([0,0])
    t = KdTree(r)
    n1 = SearchNode([10,10])
    n2 = SearchNode([-10, 10])
    n3 = SearchNode([20,5])
    n4 = SearchNode([20,10])
    t.add(n1)
    t.add(n2)
    t.add(n3)
    t.add(n4)

    s = SearchNode([-12,0])
    result = t.nearest_node(s)

    assert(result.position == n2.position)

if __name__ == '__main__':
    main()

