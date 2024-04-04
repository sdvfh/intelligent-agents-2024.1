import sys
from astar import Astar

def main(start_node, end_node):

    astar = Astar("../data/real_distances.csv", "../data/straight_line_distances.csv", "../data/node_lines.yaml")
    
    astar.calculate_A_star(start_node, end_node)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python [filename] [start node] [final node]")
        sys.exit(1)
    
    start_node = sys.argv[1]
    end_node = sys.argv[2]
    main(start_node, end_node)
