import math

class Node:
    def __init__(self, position:list, parent=None, left=None, right=None):
        self.position = position
        self.parent = parent
        self.left = left
        self.right = right

class BoundingBox:
      def __init__(self, position, distance):
          self.min = [position[0] - distance, position[1] - distance]
          self.max = [position[0] + distance, position[1] + distance]

class KdTree:
    def __init__(self, position:list):
      self.root = Node(position)
      self.k = len(self.root.position)
      # used for neighborhood search
      self.nearest_positions = []
      self.position_boundary = None

    def __add(self, position:list, root:Node, depth):
        axis = depth % self.k
        if root.position[axis] > position[axis]: # we want to insert to the left
            if root.left == None:
                root.left = Node(position, root)
                return
            else: # Node already exists, recurse
                self.__add(position, root.left, depth + 1)
        else:
            if root.right == None:
                root.right = Node(position, root)
                return
            else:
                self.__add(position, root.right, depth + 1)
  
    def add(self, position):
        root = self.root
        depth = 0
        self.__add(position, root, depth)
        
    def __dist(self, first:list, second:list):
        x1, y1 = first
        x2, y2 = second
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def __closer_distance(self, pivot:list, n1:Node, n2:Node):
        ''' Helper function to return the node n1 or n2 which is closer to pivot'''
        if n1 == None:
            return n2
        if n2 == None:
            return n1
        
        d1 = self.__dist(pivot, n1.position)
        d2 = self.__dist(pivot, n2.position)
        
        if d1 < d2:
            return n1
        else:
            return n2        
        
        
    def __nearest_position(self, root:Node, position:list, depth):
        if root is None:
            return None
        axis = depth % self.k
        next_root = None
        opposite_root = None
        
        if position[axis] < root.position[axis]:
            next_root = root.left
            opposite_root = root.right
        else:
            next_root = root.right
            opposite_root = root.left
        
        best = self.__closer_distance(
            position, 
            self.__nearest_position(next_root, position, depth +1),
            root)
        
        if (self.__dist(position, best.position) > abs(position[axis] - root.position[axis])):
            best = self.__closer_distance(
                position, 
                self.__nearest_position(opposite_root, position, depth +1),
                best)
        return best
    
    def nearest_position(self, position):
        root = self.root
        depth = 0
        return self.__nearest_position(root, position, depth).position
    
    def __surrounding_positions(self, root:Node, position, distance, depth):
        if root is None:
            return None

        if self.__dist(position, root.position) <= distance:
            self.nearest_positions.append(root.position)
        
        axis = depth % self.k

        if self.position_boundary.min[axis] < root.position[axis] and self.position_boundary.max[axis] < root.position[axis]:
            # search left node
            self.__surrounding_positions(root.left, position, distance, depth + 1)
        elif self.position_boundary.min[axis] > root.position[axis] and self.position_boundary.max[axis] > root.position[axis]:
            # search right node
            self.__surrounding_positions(root.right, position, distance, depth + 1)
        else:
            # check both
            self.__surrounding_positions(root.left, position, distance, depth + 1)
            self.__surrounding_positions(root.right, position, distance, depth + 1)    

    def surrounding_positions(self, position, distance):
        root = self.root
        depth = 0
        self.nearest_positions = []
        self.position_boundary = BoundingBox(position, distance)
        self.__surrounding_positions(root, position, distance, depth)
        return self.nearest_positions
