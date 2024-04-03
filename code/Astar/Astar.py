from .data_loader import DataLoader


class Astar():
    def __init__(self, real_dist_path, straightline_dist_path):
        self.neighbors_dict, self.straightline_distances = DataLoader(real_dist_path,
                                                                      straightline_dist_path).return_dicts()
        self.frontier = {}
        self.start_node = None
        self.goal_node = None

    def neighbors(self, node):
        return list(self.neighbors_dict[node].keys())

    def straight_distance_between(self, n1, n2):
        if n1 == n2:
            return 0
        return self.straightline_distances[n1][n2]

    def real_distance_between(self, n1, n2):
        if n1 == n2:
            return 0
        return self.neighbors_dict[n1][n2]

    def heuristic_cost_estimate(self, current_total_distance, current_node, next_node, goal_node):
        # Current total distance + real distance between current node and next node + straight distance between next node and goal node
        new_total_distance = current_total_distance + self.real_distance_between(current_node, next_node)
        heuristic_cost = self.straight_distance_between(next_node, goal_node)
        node_cost = new_total_distance + heuristic_cost
        return node_cost, heuristic_cost, new_total_distance

    def create_initial_frontier(self):
        initial_frontier = self.neighbors(self.start_node)
        for node in initial_frontier:
            node_cost, heuristic_cost, new_total_distance = self.heuristic_cost_estimate(0, self.start_node, node,
                                                                                         self.goal_node)
            self.frontier[node] = {'f': node_cost, 'h': heuristic_cost, 'g': new_total_distance,
                                   'full_path': [self.start_node]}

    def calculate_A_star(self, start_node, goal_node):
        self.start_node = start_node
        self.goal_node = goal_node
        self.create_initial_frontier()
        while self.frontier:
            print(f'Current frontier nodes: {list(self.frontier.keys())}')
            current_node = min(self.frontier, key=lambda k: self.frontier[k]['f'])
            print(
                f'selected node: {current_node} | f: {self.frontier[current_node]["f"]} | h: {self.frontier[current_node]["h"]} | g: {self.frontier[current_node]["g"]} | path: {self.frontier[current_node]["full_path"]}')
            if current_node == self.goal_node:
                print(
                    f'Found goal node: {current_node} | path: {self.frontier[current_node]["full_path"]} | f: {self.frontier[current_node]["f"]} | h: {self.frontier[current_node]["h"]} | g: {self.frontier[current_node]["g"]}')
                break
            current_node_cost = self.frontier[current_node]['f']
            current_node_path = self.frontier[current_node]['full_path']
            del self.frontier[current_node]
            for neighbor_node in self.neighbors(current_node):
                node_cost, heuristic_cost, new_total_distance = self.heuristic_cost_estimate(current_node_cost,
                                                                                             current_node,
                                                                                             neighbor_node,
                                                                                             self.goal_node)
                self.frontier[neighbor_node] = {'f': node_cost, 'h': heuristic_cost, 'g': new_total_distance,
                                                'full_path': current_node_path + [current_node]}
