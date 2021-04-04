class SearchNode:
    def __init__(self, position:[], parent=None, distance=0):
        self.position = position
        self.parent = parent
        # keeping track of distance
        self.distance = distance
        self.path = None # Dubins path