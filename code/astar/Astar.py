from .data_loader import DataLoader

class Astar():
    def __init__(self, real_dist_path, direct_dist_path,node_lines_path):
        self.start_node = None
        self.goal_node = None
        self._frontier = {}
        self._real_dist, self._direct_dist,self.node_lines = DataLoader(real_dist_path, direct_dist_path,node_lines_path).return_dicts()
        

    def calculate_A_star(self, start_node, goal_node):
        self.start_node = start_node
        self.goal_node = goal_node
        self.create_initial_frontier()

        while True:            

            # Sort the items of the dictionary based on the 'f' value
            sorted_items = sorted(self._frontier.items(), key=lambda x: x[1]['f'])

            # Create an auxiliary dictionary with the sorted order
            aux_dict = {key: value['f'] for key, value in sorted_items}

            print(f'Current frontier nodes: {aux_dict}')

            current_node = min(self._frontier, key=lambda k: self._frontier[k]["f"])

            f = self._frontier[current_node]["f"]
            g = self._frontier[current_node]["g"]
            h = self._frontier[current_node]["h"]
            full_path = self._frontier[current_node]["full_path"]

            found_node = current_node == self.goal_node

            if found_node:
                text = "Found goal"
            else:
                text = "Selected"


            print(f"{text} node: {current_node} | f: {f:.2f} | g: {g:.2f} | h: {h:.2f} | path: {full_path}\n")

            if found_node:
                break

            del self._frontier[current_node]

            for neighbor_node in self._get_neighbors(current_node):
                line_change = self._verify_line_change(full_path[-1],current_node,neighbor_node)
                node_cost, heuristic_cost, new_total_distance = self._heuristic_cost_estimate(
                    f,
                    current_node,
                    neighbor_node,
                    self.goal_node,
                    line_change
                )
                self._update_frontier(
                    node=neighbor_node,
                    f=node_cost,
                    g=new_total_distance,
                    h=heuristic_cost,
                    full_path=full_path + [current_node]
                )


    def create_initial_frontier(self):
        initial_frontier = self._get_neighbors(self.start_node)
        for node in initial_frontier:
            node_cost, heuristic_cost, new_total_distance = self._heuristic_cost_estimate(
                0,
                self.start_node,
                node,
                self.goal_node
            )
            self._update_frontier(
                node=node,
                f=node_cost,
                g=new_total_distance,
                h=heuristic_cost,
                full_path=[self.start_node]
            )

    def _get_neighbors(self, node):
        return list(self._real_dist[node].keys())

    def _update_frontier(self, node, f, g, h, full_path):
        self._frontier[node] = {
            # f(n) = g(n) + h(n)
            "f": f,
            # g(n) = distancia de n ao no inicial
            "g": g,
            # h(n) = distancia estimada de n ao no final
            "h": h,
            "full_path": full_path
        }

    def _straight_distance_between(self, n1, n2):
        if n1 == n2:
            return 0
        return self._direct_dist[n1][n2]

    def _real_distance_between(self, n1, n2):
        if n1 == n2:
            return 0
        return self._real_dist[n1][n2]

    def _verify_line_change(self,previous_node,current_node,next_node):

        # Intersecção entre as linhas do nó anterior e do nó atual - linhas que podemos estar chegando
        arrival_lines = self.node_lines[previous_node].intersection(self.node_lines[current_node])

        # Intersecção entre as linhas do nó atual e do próximo nó - linhas pelas quais podemos partir
        departure_lines = self.node_lines[current_node].intersection(self.node_lines[next_node])

        # Se não há sobreposição entre as linhas de chegada e partida, precisamos de uma baldeação
        if arrival_lines.isdisjoint(departure_lines):
            print(f"Baldeação necessária para ir de {current_node} para {next_node}, vindo de {previous_node}")
            return True
        return False 
    
    def _heuristic_cost_estimate(self, current_total_distance, current_node, next_node, goal_node,line_change=False):
        # Current total distance + real distance between current node and next node + straight distance between next node and goal node
        new_total_distance = current_total_distance + self._real_distance_between(current_node, next_node)
        if line_change:
            new_total_distance += 3
        heuristic_cost = self._straight_distance_between(next_node, goal_node)
        node_cost = new_total_distance + heuristic_cost
        return round(node_cost,2), round(heuristic_cost,2), round(new_total_distance,2)
