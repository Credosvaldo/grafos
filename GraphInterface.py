from abc import ABC, abstractmethod


class GraphInterface(ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def print_weight_matrix(self):
        pass

    @abstractmethod
    def show_some(self):
        pass

    @abstractmethod
    def add_edge(self, predecessor: str, successor: str, weight: float = 1, name: str = None):
        pass

    @abstractmethod
    def remove_edge_by_name(self, name: str):
        pass

    @abstractmethod
    def remove_all_edge_by_nodes(self, predecessor: str, successor: str):
        pass

    @abstractmethod
    def add_node(self, name: str = None, weight: float = 0):
        pass

    @abstractmethod
    def remove_node(self, name: str):
        pass

    @abstractmethod
    def thers_node_adjacente(self, predecessor: str, successor: str):
        pass

    @abstractmethod
    def thers_edge_adjacence(self, ed1: str, ed2: str):
        pass

    @abstractmethod
    def thers_edge_by_name(self, name: str):
        pass

    @abstractmethod
    def thers_edge_by_nodes(self, predecessor: str, successor: str):
        pass

    @abstractmethod
    def get_edge_count(self):
        pass

    @abstractmethod
    def get_node_count(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def is_complete(self):
        pass

    @abstractmethod
    def make_revert_graph(self):
        pass

    @abstractmethod
    def print_revert_graph(self):
        pass

    @abstractmethod
    def make_underlying_graph(self):
        pass

    @abstractmethod
    def print_underlying_graph(self):
        pass