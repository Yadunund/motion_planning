# Motion Planning
Implementations of path planning algorithms

## Grid based planners
Here we compare the performance of Dijkstras and AStar algorithms in finding a path from a start (yellow tile) to the goal (red tile). By default, the planner aims to find a path from the top-left corner tile to the top-right corner tile of the grid. It is assumed that the edges of the grid have equal weights.


usage:
```
Dijkstras: python3 grid_planners/main -n 10 -a dijsktras
Astar: python3 grid_planners/main -n 10 -a astar
```

<div align=center>
<table>
  <tr>
    <td><img src="https://github.com/Yadunund/motion_planning/blob/master/media/dijkstras.png" alt="dijkstra" width="400"/></a></td>
    <td><img src="https://github.com/Yadunund/motion_planning/blob/master/media/astar.png" alt="astar" width="400"/></a></td>
  </tr>
</table>
</div>

## Free space planners

usage:
```
RRT: python3 free_space_planners/main.py -a rrt
RRT*: python3 free_space_planners/main.py -a rrtstar
Informed-RRT*: python3 free_space_planners/main.py -a irrtstar
```

<div align=center>
<table>
  <tr>
    <td><img src="https://github.com/Yadunund/motion_planning/blob/master/media/rrt.png" alt="rrt" width="400"/></a></td>
    <td><img src="https://github.com/Yadunund/motion_planning/blob/master/media/rrtstar.png" alt="rrtstar" width="400"/></a></td>
  </tr>
</table>
<table>
  <tr>
    <td>
      Path from [15, 15] to [190, 190] found with distance 388.033 after expanding 7000 nodes rrt ran for 0.390s
    </td>
    <td>
      Path from [15, 15] to [190, 190] found with distance 271.359 after expanding 7000 nodes rrtstar ran for 1.726s
    </td>
  </tr>
</table>
<table>
  <tr>
    <td><img src="https://github.com/Yadunund/motion_planning/blob/master/media/informed_rrtstar.png" alt="rrt" width="400"/></a></td>
  </tr>
</table>
<table>
  <tr>
    <td>
      Path from [15, 15] to [190, 190] found with distance 256.380 after expanding 7000 nodes irrtstar ran for 4.364s
    </td>
  </tr>
</table>
</div>


