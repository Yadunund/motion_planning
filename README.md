# Motion Planning
Implementations of path planning algorithms

## Grid based planners
Here we compare the performance of Dijkstras and AStar algorithms in finding a path from a start (yellow tile) to the goal (red tile). By default, the planner aims to find a path from the top-left corner tile to the top-right corner tile of the grid. It is assumed that the edges of the grid have equal weights.


usage:
```
python3 grid_planners/main.py -h
```

#### Path planning with Dijkstras algorithm on a 2D grid
```
python3 grid_planners/main -n 10 -a dijsktras
```

![](media/dijkstras.png)

Terminal output:
```
Solving using Dijkstras...
    Found goal (0, 7) with distance 16.898
Solution found in 0.036817073822021484 seconds
Path found from (0, 0) to (0, 7) after expanding 85 nodes!
Path: [(0, 0), (1, 0), (2, 0), (3, 1), (4, 2), (5, 3), (6, 4), (7, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (1, 6), (0, 7)]

```

#### Path planning with Astar algorithm on a 2D grid

```
python3 grid_planners/main -n 10 -a astar
```

![](media/astar.png)

Terminal output:
```
Solving using A*...
    Found goal (0, 7) with distance 16.897
Solution found in 0.0024843215942382812 seconds
Path found from (0, 0) to (0, 7) after expanding 46 nodes!
Path: [(0, 0), (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 4), (7, 5), (6, 6), (5, 6), (4, 6), (3, 6), (2, 6), (1, 7), (0, 7)]



```

## Free space planners

usage:
```
python3 free_space_planners/main.py -h
```

### Path planning with RRT in free space with obstacles

```
python3 free_space_planners/main.py -a rrt
```
```
Path from [15, 15] to [190, 190] found with distance 388.033102354826 after expanding 7000 nodes
 rrt ran for 0.3900134563446045s
```

![](media/rrt.png)


### Path planning with RRT* in free space with obstacles

```
python3 free_space_planners/main.py -a rrtstar
```

```
Path from [15, 15] to [190, 190] found with distance 271.3592691760186 after expanding 7000 nodes
 rrtstar ran for 1.7262961864471436s
```

![](media/rrtstar.png)

### Path planning with Informed-RRT* in free space with obstacles

```
python3 free_space_planners/main.py -a irrtstar
```

```
Path from [15, 15] to [190, 190] found with distance 256.3809869882846 after expanding 7000 nodes
 irrtstar ran for 4.364379405975342s

```

![](media/informed_rrtstar.png)


