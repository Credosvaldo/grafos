from typing import List, Dict, Tuple
from models.DFSNode import DFSNode
from models.TarjansNode import TarjansNode

class Grafo:
    def add_node(self, name: str, weight: float = 1.0):
        pass

    def remove_node(self, name: str):
        pass

    def add_edge(self, predecessor: str, successor: str, weight: float = 1, name: str = None):
        pass

    def remove_edge_by_name(self, name: str):
        pass

    def remove_all_edges_by_nodes(self, predecessor: str, successor: str):
        pass

    def thers_node_adjacency(self, predecessor: str, successor: str):
        pass

    def thers_only_one_edge_btwn_nodes(self, predecessor: str, successor: str):
        pass

    def thers_edge_adjacency(self, edge1: str, edge2: str):
        pass

    def thers_edge_by_name(self, name: str):
        pass

    def thers_edge_by_nodes(self, predecessor: str, successor: str):
        pass

    def get_edge_count(self):
        pass

    def get_node_count(self):
        pass

    def is_empty(self):
        pass

    def is_complete(self):
        pass

    def is_simple(self):
        pass

    def is_connected(self):
        pass

    def get_bridge(self):
        pass

    def is_bridge(self, edge_name: str):
        pass

    def get_articulations(self):
        pass

    def is_articulation(self, node_name: str):
        pass

    def get_euler_path(self, by_tarjan: bool = True):
        pass

    def get_edges_by_node(self, node_name: str):
        pass

    def get_all_nodes_degree(self):
        pass

    def make_revert_graph(self):
        pass

    def print_revert_graph(self):
        pass

    def make_underlying_graph(self):
        pass

    def print_underlying_graph(self):
        pass

    def to_graph(self, path: str):
        pass

    def to_xml(self):
        pass

    def connectivity_degree(self):
        pass

    def reachable(self, v1: str, v2: str, results: Dict[str, Dict[str, DFSNode]]):
        pass

    def kosaraju(self):
        pass

    def _tarjan_dfs(self, node_name: str, result: Dict[str, TarjansNode], bridges: List[str], time: List[int]):
        pass

    def get_bridge_by_tarjan(self):
        pass

    def is_bridge_by_tarjan(self, edge_name: str):
        pass