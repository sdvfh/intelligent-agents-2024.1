from astar import Astar

astar = Astar("../data/real_distances.csv", "../data/straight_line_distances.csv","../data/node_lines.yaml")

astar.calculate_A_star("E1", "E5")
