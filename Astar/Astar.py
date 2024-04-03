import pandas as pd
import numpy as np
from London.data_loader import DataLoader

class Astar():
    def __init__(self,real_dist_path,straightline_dist_path):
        self.neighbors_dict,self.straightline_distances,self.node_lines = DataLoader(real_dist_path,straightline_dist_path).return_dicts()
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
    
    def create_initial_frontier(self):
        initial_frontier = self.neighbors(self.start_node)
        for node in initial_frontier:
            node_cost,heuristic_cost,new_total_distance = self.heuristic_cost_estimate(0,self.start_node,node,self.goal_node,line_change=False)
            self.frontier[node] = {'f': node_cost,'h': heuristic_cost,'g': new_total_distance,'full_path': [self.start_node]}
  
    def verify_line_change(self,previous_node,current_node,next_node):
        """
        Verifica, a partir do nó anterior e da variável node_lines, se a linha de metrô
        pela qual estamos chegando no nó atual é diferente da linha pela qual partiremos
        para o próximo nó. Se as linhas forem diferentes, retorna o tempo de troca de linha;
        caso contrário, retorna 0.
        """
        
        # Intersecção entre as linhas do nó anterior e do nó atual - linhas que podemos estar chegando
        arrival_lines = self.node_lines[previous_node].intersection(self.node_lines[current_node])
        
        # Intersecção entre as linhas do nó atual e do próximo nó - linhas pelas quais podemos partir
        departure_lines = self.node_lines[current_node].intersection(self.node_lines[next_node])
        
        # Se não há sobreposição entre as linhas de chegada e partida, precisamos de uma baldeação
        if arrival_lines.isdisjoint(departure_lines):
            print(f"Baldeação necessária para ir de {current_node} para {next_node}, vindo de {previous_node}")
            return True
        return False 
        
    def heuristic_cost_estimate(self, current_total_distance,current_node, next_node,goal_node,line_change):
        # Current total distance + real distance between current node and next node + straight distance between next node and goal node
        new_total_distance = current_total_distance + self.real_distance_between(current_node,next_node)
        if line_change:
            new_total_distance += 3
        heuristic_cost = self.straight_distance_between(next_node,goal_node)
        node_cost = new_total_distance + heuristic_cost
        return node_cost,heuristic_cost,new_total_distance

    def calculate_A_star(self,start_node,goal_node):
        self.start_node = start_node
        self.goal_node = goal_node
        self.create_initial_frontier()
        while self.frontier:
            print(f'Current frontier nodes: {list(self.frontier.keys())}')
            current_node = min(self.frontier, key=lambda k: self.frontier[k]['f'])
            print(f'selected node: {current_node} | f: {self.frontier[current_node]["f"]:.2f} | h: {self.frontier[current_node]["h"]:.2f} | g: {self.frontier[current_node]["g"]:.2f} | path: {self.frontier[current_node]["full_path"]}')
            if current_node == self.goal_node:
                print(f'Found goal node: {current_node} | path: {self.frontier[current_node]["full_path"]} | f: {self.frontier[current_node]["f"]:.2f} | h: {self.frontier[current_node]["h"]:.2f} | g: {self.frontier[current_node]["g"]:.2f}')
                break
            current_node_cost = self.frontier[current_node]['f']
            current_node_path = self.frontier[current_node]['full_path']
            del self.frontier[current_node]
            for neighbor_node in self.neighbors(current_node):
                if len(current_node_path) > 1:
                    line_change = self.verify_line_change(current_node_path[-1],current_node,neighbor_node)
                else:
                    line_change = False
                node_cost,heuristic_cost,new_total_distance = self.heuristic_cost_estimate(current_node_cost,current_node,neighbor_node,self.goal_node,line_change)
                self.frontier[neighbor_node] = {'f': node_cost,'h': heuristic_cost,'g': new_total_distance,'full_path': current_node_path + [current_node]}
