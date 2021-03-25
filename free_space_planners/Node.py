class SearchNode:
    def __init__(self, position:[], parent=None, left=None, right=None):
        self.position = position
        self.parent = parent
        # for use in Kdtree
        self.left = left
        self.right = right