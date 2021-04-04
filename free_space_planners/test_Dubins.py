import dubins

import matplotlib.pyplot as plt

def main():
  start = (0.0, 0.0, 1.57)
  goal = (10, 5, -1.57)
  r = 0.5
  d = dubins.shortest_path(start, goal, r)
  print(f"Generate dubins curve of type {d.path_type()} with length {d.path_length()}")
  c, dists = d.sample_many(0.1)
  print(f"Sampled {len(c)} points")
  x = [p[0] for p in c]
  y = [p[1] for p in c]
  plt.plot(x, y, 'g-')
  plt.show()
if __name__ == '__main__':
    main()