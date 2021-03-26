class SearchNode:
    def __init__(self, position:[], parent=None, distance=0, left=None, right=None):
        self.position = position
        self.parent = parent
        # for use in Kdtree
        self.left = left
        self.right = right

        # keeping track of distance
        self.distance = distance