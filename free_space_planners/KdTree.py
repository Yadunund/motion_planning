from Node import SearchNode
import math

class KdTree:
    def __init__(self, root_node:SearchNode):
      self.root = root_node
      self.k = len(root_node.position)

    def __add(self, node:SearchNode,root:SearchNode, depth):
        axis = depth % self.k
        if root.position[axis] > node.position[axis]: # we want to insert to the left
            if root.left == None:
                root.left = SearchNode(node.position, root, node.distance)
                return
            else: # Node already exists, recurse
                self.__add(node, root.left, depth + 1)
        else:
            if root.right == None:
                root.right = SearchNode(node.position, root, node.distance)
                return
            else:
                self.__add(node, root.right, depth + 1)
  
    def add(self, node:SearchNode):
        root = self.root
        depth = 0
        self.__add(node, root, depth)
        
    def __dist(self, first:SearchNode, second:SearchNode):
        x1, y1 = first.position
        x2, y2 = second.position
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def __closer_distance(self, pivot:SearchNode, n1:SearchNode, n2:SearchNode):
        ''' Helper function to return the node n1 or n2 which is closer to pivot'''
        if n1 == None:
            return n2
        if n2 == None:
            return n1
        
        d1 = self.__dist(pivot, n1)
        d2 = self.__dist(pivot, n2)
        
        if d1 < d2:
            return n1
        else:
            return n2        
        
        
    def __nearest_node(self, root:SearchNode, node:SearchNode, depth):
        if root is None:
            return None
        axis = depth % self.k
        next_root = None
        opposite_root = None
        
        if node.position[axis] < root.position[axis]:
            next_root = root.left
            opposite_root = root.right
        else:
            next_root = root.right
            opposite_root = root.left
        
        best = self.__closer_distance(
            node, 
            self.__nearest_node(next_root, node, depth +1),
            root)
        
        if (self.__dist(node, best) > abs(node.position[axis] - root.position[axis])):
            best = self.__closer_distance(
                node, 
                self.__nearest_node(opposite_root, node, depth +1),
                best)
        return best
    
    def nearest_node(self, node:SearchNode):
        root = self.root
        depth = 0
        return self.__nearest_node(root, node, depth)
    
