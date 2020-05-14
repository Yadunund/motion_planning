# Motion Planning
Implementations of path planning algorithms

## Grid based planners
Here we compare the performance of Dijkstras and AStar algorithms in finding a path from a start (yellow tile) to the goal (red tile).

#### Path planning with Dijkstras algorithm on a 2D grid
![](media/dijkstras.png)


#### Path planning with Astar algorithm on a 2D grid

![](media/astar.png)

Usage:
```
cd grid_planners/
chmod +x main.py
./main -n 10 -a dijsktras
./main -n 10 -a astar
```
where -n is the dimension of the grid and -a specifies the algorithm used to find the shortest path. By default, the planner aims to find a path from the top-left corner tile to the top-right corner tile of the grid. It is assumed that the edges of the grid have equal weights.

