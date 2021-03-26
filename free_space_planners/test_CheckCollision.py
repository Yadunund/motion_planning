from CheckCollision import TrainglePointCollision
from Shape import ConvexShape

shape = ConvexShape([[0,0], [5, 10], [10, 0]])

point_in_shape = [5, 5]
point_out_shape = [50,50]

assert(TrainglePointCollision(shape, point_in_shape))
assert (not TrainglePointCollision(shape, point_out_shape))