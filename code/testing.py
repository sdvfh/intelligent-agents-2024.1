from astar import Astar

astar = Astar("../data/real_distances.csv", "../data/straight_line_distances.csv")

astar.calculate_A_star("E1", "E5")
