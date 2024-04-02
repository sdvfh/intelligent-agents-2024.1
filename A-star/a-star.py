import pandas as pd

class a_star():
    def __init__(self):
        self.graph = {}
        self.real_dist_path = ""
        self.straightline_dist_path = ""

    def load_data(self,real_dist_path,straightline_dist_path):
        real_dist = pd.read_csv(self.real_dist_path)
        straightline_dist = pd.read_csv(self.straightline_dist_path)
        return real_dist, straightline_dist
    
    def neighbors(self, node):
        return self.graph[node]
    
    def straight_distance_between(self, n1, n2):
        pass

    def real_distance_between(self, n1, n2):
        pass

    def heuristic_cost_estimate(self, current, goal):
        pass