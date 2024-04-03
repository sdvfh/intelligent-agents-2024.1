import pandas as pd
import numpy as np


class DataLoader():
    def __init__(self, real_dist_path, direct_dist_path):
        # Dataframe com distancias reais para calcular g(n) = distancia de n ao no inicial
        real_dist = self._load_csv(real_dist_path)

        # Dataframe com distancias em linha reta h(n) = distancia estimada de n ao nó final
        direct_dist = self._load_csv(direct_dist_path)

        self.real_dist = {"df": real_dist, "dict": self._df_to_dict(real_dist)}
        self.direct_dist = {"df": direct_dist, "dict": self._df_to_dict(direct_dist)}

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
    def _df_to_dict(df):
        actual_dict = {}
        for current_node, line in df.iterrows():
            line = line[line > 0]
            for neighbour, distance in line.items():
                if current_node not in actual_dict:  # Se o nó atual não está no dicionário de vizinhos
                    actual_dict[current_node] = {}
                actual_dict[current_node][neighbour] = distance
        return actual_dict
