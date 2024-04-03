import pandas as pd
import numpy as np
import yaml
pd.set_option('future.no_silent_downcasting', True)

class DataLoader():
    def __init__(self, real_dist_path, direct_dist_path,node_lines_path):
        # Dataframe com distancias reais para calcular g(n) = distancia de n ao no inicial
        real_dist = self._load_csv(real_dist_path)

        # Dataframe com distancias em linha reta h(n) = distancia estimada de n ao no final
        direct_dist = self._load_csv(direct_dist_path)

        self._real_dist = self._df_to_dict(real_dist)
        self._direct_dist = self._df_to_dict(direct_dist)
        self._node_lines = self._load_yaml(node_lines_path)

    @staticmethod
    def _load_csv(path):
        df = pd.read_csv(path, index_col="Unnamed: 0").replace('x', np.nan).astype(np.float64)
        df.index.names = ["Node"]
        df = df.fillna(0.0)
        # Replicar a matriz para ser simetrica
        # De https://stackoverflow.com/questions/16444930/copy-upper-triangle-to-lower-triangle-in-a-python-matrix
        df = df + df.T - np.diag(np.diag(df))
        return df

    @staticmethod
    def _df_to_dict(df,mean_speed = 40):
        actual_dict = {}
        for current_node, line in df.iterrows():
            line = line[line > 0]
            for neighbour, distance in line.items():
                if current_node not in actual_dict:  # Se o no atual nao esta no dicionario de vizinhos
                    actual_dict[current_node] = {}
                # Tempo = distancia / velocidade media * 60 para transformar em minutos
                actual_dict[current_node][neighbour] = (distance / mean_speed) * 60
        
        return actual_dict
    
    @staticmethod
    def _load_yaml(path):
        with open(path, 'r') as stream:
            node_lines_dict = yaml.safe_load(stream)
        # Trocando listas por set para facilitar análise posterior
        node_lines_dict = {key: set(value) for key, value in node_lines_dict.items()}
        return node_lines_dict
    
    def return_dicts(self):
        return self._real_dist, self._direct_dist, self._node_lines