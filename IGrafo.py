from typing import List, Dict, Tuple
from models.DFSNode import DFSNode
from models.TarjansNode import TarjansNode


class IGrafo:
    def add_node(self, name: str, weight: float = 1.0):  # GrafoMa, GrafoLA , GrafoMi
        pass

    def remove_node(self, name: str):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def add_edge(
        self, predecessor: str, successor: str, weight: float = 1, name: str = None
    ):  # GrafoMa , GrafoLA, GrafMi
        pass

    def remove_edge_by_name(self, name: str):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def remove_all_edges_by_nodes(
        self, predecessor: str, successor: str
    ):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def thers_node_adjacency(
        self, predecessor: str, successor: str
    ):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def thers_only_one_edge_btwn_nodes(
        self, predecessor: str, successor: str
    ):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def thers_edge_adjacency(
        self, edge1: str, edge2: str
    ):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def thers_edge_by_name(self, name: str):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def thers_edge_by_nodes(
        self, predecessor: str, successor: str
    ):  # GrafoMa  , GrafoLA , GrafoMi
        pass

    def get_edge_count(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def get_node_count(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def is_empty(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def is_complete(self):  # GrafoMa , GrafoLA  , GrafoMi
        pass

    def is_simple(self):  # GrafoMa  , GrafoLA , GrafoMi
        pass

    def is_connected(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def get_bridge(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def is_bridge(self, edge_name: str):  # GrafoMa , GrafoLA, GrafoMi
        pass

    def get_articulations(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def is_articulation(self, node_name: str):  # GrafoMa , GrafoLA
        pass

    def get_euler_path(self, by_tarjan: bool = True):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def get_edges_by_node(self, node_name: str):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def get_all_nodes_degree(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def make_revert_graph(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def make_underlying_graph(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def to_graph(self, path: str):  # GrafoMa , GrafoLA
        pass

    def to_xml(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def connectivity_degree(self):  # GrafoMa , GrafoLA, GrafoMi
        pass

    def reachable(
        self, v1: str, v2: str, results: Dict[str, Dict[str, DFSNode]]
    ):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def kosaraju(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def _tarjan_dfs(
        self,
        node_name: str,
        result: Dict[str, TarjansNode],
        bridges: List[str],
        time: List[int],
    ):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def get_bridge_by_tarjan(self):  # GrafoMa , GrafoLA , GrafoMi
        pass

    def is_bridge_by_tarjan(self, edge_name: str):  # GrafoMa , GrafoLA , GrafoMi
        pass
