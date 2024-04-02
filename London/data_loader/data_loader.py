import pandas as pd
import numpy as np

class DataLoader():
    def __init__(self,real_dist_path,straightline_dist_path):
        self.neighbors_dict = {}
        self.straightline_distances = {}
        # Dataframe com distancias reais para calcular g(n) = distância de n ao nó inicial
        self.real_dist_df = pd.read_csv(real_dist_path).rename(columns={'Unnamed: 0': 'node'})
        # Dataframe com distancias em linha reta h(n) = distância estimada de n ao nó final
        self.straightline_dist_df = pd.read_csv(straightline_dist_path).rename(columns={'Unnamed: 0': 'node'})

        self.real_dist_df = self.real_dist_df.replace('x', np.nan)
        self.straightline_dist_df = self.straightline_dist_df.replace('x', np.nan)

        self.__load_neighbors_dict()
        self.__load_straightline_distances()
    
    def __load_neighbors_dict(self):
        """
        Carrega o dicionário de vizinhos a partir do dataframe de distâncias reais
        """
        self.neighbors_dict = {}
        for idx in self.real_dist_df.index: # Para cada linha do dataframe
            row = self.real_dist_df.loc[idx].dropna() # Pega a linha e remove os valores nulos
            current_node = row['node'] # Pega o nome do nó analisado atualmente
            for neighbour, distance in row.drop(['node']).dropna().items(): # Para cada vizinho do nó atual
                if current_node not in self.neighbors_dict: # Se o nó atual não está no dicionário de vizinhos
                    self.neighbors_dict[current_node] = {}  # Adiciona o nó atual no dicionário
                self.neighbors_dict[current_node][neighbour] = float(distance) # Adiciona o vizinho e a distância no dicionário

    def __load_straightline_distances(self):
        """
        Carrega o dicionário de distâncias em linha reta a partir do dataframe de distâncias em linha reta
        """
        self.straightline_distances = {}
        for idx in self.straightline_dist_df.index:
            row = self.straightline_dist_df.loc[idx].dropna()
            current_node = row['node']
            for neighbour, distance in row.drop(['node']).dropna().items():
                if current_node not in self.straightline_distances:
                    self.straightline_distances[current_node] = {}
                self.straightline_distances[current_node][neighbour] = float(distance)

    def return_dicts(self):
        return self.neighbors_dict,self.straightline_distances