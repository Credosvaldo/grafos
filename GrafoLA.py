from typing import Dict, List, Tuple
from DFSNode import DFSNode
from ExcludedEdge import ExcludedEdge
from NodeLA import NodeLA
from datetime import datetime
import copy


class GrafoLA:

    def __init__(
        self,
        DIRECTED: bool = True,
        num_nodes: int = 0,
        nodes: List[NodeLA] = [],  # replace to tupla
    ):

        self.nodes_map: Dict[str, NodeLA] = {}
        self.edges_map: Dict[str, Tuple[str, str, float]] = (
            {}
        )  # predecessor , successor, weight
        self.DIRECTED = DIRECTED
        self.list_adjacency: Dict[str, List[NodeLA]] = {}
        self.create_adjacency_list(num_nodes, nodes)

    def create_adjacency_list(self, num_nodes: int, nodes: List[NodeLA]):
        if nodes == [] and num_nodes == 0:
            return {}

        if len(nodes) != num_nodes and nodes != []:
            raise ValueError(
                "Number of nodes does not match the number of nodes provided"
            )

        if nodes == []:
            for i in range(num_nodes):

                new_edge_name = len(self.edges_map) + 1
                name = None

                while name is None or name in self.nodes_map:
                    name = str(new_edge_name)
                    new_edge_name += 1

                name = str(name)
                self.add_node(name, 0)

    def add_node(self, name: str, weight: float):
        """
        Adds a new node to the graph.

        Parameters:
        name (str): The name of the node to be added.
        weight (float): The weight of the node to be added.

        Raises:
        ValueError: If a node with the given name already exists in the graph.
        """
        if name not in self.nodes_map:
            self.list_adjacency[name] = []
            self.nodes_map[name] = NodeLA(weight, name)
        else:
            raise ValueError("NodeLA name already exists")

    def remove_node(self, name: str):
        """
        Removes a node and its associated edges from the graph.

        Args:
            name (str): The name of the node to be removed.

        Raises:
            ValueError: If the node name is not found in the graph.

        This method removes the specified node from the nodes_map and list_adjacency.
        It also removes any edges in other nodes' adjacency lists that point to the removed node.
        """
        if name in self.nodes_map:
            self.nodes_map.pop(name)
            self.list_adjacency.pop(name)
            for node in self.list_adjacency:
                self.list_adjacency[node] = list(
                    filter(lambda x: x.name != name, self.list_adjacency[node])
                )
        else:
            raise ValueError("NodeLA name not found")

    # Check loop e parallel edge
    def add_edge(self, predecessor: str, successor: str, weight: float, name: str):
        """
        Adds an edge to the graph.
        Parameters:
        predecessor (str): The starting node of the edge.
        successor (str): The ending node of the edge.
        weight (float): The weight of the edge.
        name (str): The name of the edge.
        Returns:
        None
        """

        if predecessor not in self.list_adjacency:
            self.add_node(predecessor, None)
        if successor not in self.list_adjacency:
            self.add_node(successor, None)

        if name in self.edges_map:
            raise ValueError("Edge already exist")

        self.list_adjacency[predecessor].append(self.nodes_map[successor])

        if not self.DIRECTED and predecessor != successor:
            self.list_adjacency[successor].append(self.nodes_map[predecessor])

        self.edges_map[name] = (predecessor, successor, weight)

    def remove_edge(self, name: str):
        """
        Removes an edge from the graph.

        Args:
            name (str): The name of the edge to be removed.

        Raises:
            ValueError: If the edge name is not found in the graph.

        This method removes the specified edge from the edges_map.
        It also removes the edge from the adjacency list of the predecessor node.
        """
        if name in self.edges_map:
            predecessor, successor, _ = self.edges_map[
                name
            ]  # _ is the weight of the edge that we are not using
            self.list_adjacency[predecessor] = list(
                filter(
                    lambda x: x.name != successor, self.list_adjacency[predecessor]
                )  # x.name != successor
            )
            if not self.DIRECTED:
                self.list_adjacency[successor] = list(
                    filter(
                        lambda x: x.name != predecessor,
                        self.list_adjacency[successor],  # x.name != predecessor
                    )
                )
            self.edges_map.pop(name)
        else:
            raise ValueError("Edge name not found")

    def remove_all_edge_by_nodes(self, predecessor: str, successor: str):
        """
        Removes all edges between two nodes from the graph.

        Args:
            predecessor (str): The name of the predecessor node.
            successor (str): The name of the successor node.

        This method removes all edges between the predecessor and successor nodes from the graph.
        """
        for key in self.edges_map:
            v1, v2, _ = self.edges_map[
                key
            ]  # _ is the weight of the edge that we are not using
            if v1 == predecessor and v2 == successor:
                self.remove_edge(edge)

    def __str__(self):
        result = " List Adjacency\n"
        for node in self.list_adjacency:
            result += f"{node} -> "
            for neighbor in self.list_adjacency[node]:
                result += f"[{neighbor.name}] -> "
            result += "\n"
        return result

    def thers_edge_by_name(self, name: str):

        if name in self.edges_map:
            return True

        return False

    def thers_edge_by_nodes(self, predecessor: str, successor: str):

        for key in self.edges_map:
            v1, v2, _ = self.edges_map[
                key
            ]  # _ is the weight of the edge that we are not using
            if v1 == predecessor and v2 == successor:
                return True

        return False

    def is_empty(self):
        return len(self.list_adjacency) == 0

    def get_edge_count(self):
        return len(self.edges_map)

    def get_node_count(self):
        return len(self.list_adjacency)

    def thers_node_adjacency(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.list_adjacency or v2 not in self.list_adjacency:
            raise ValueError("nodes does not exist")

        for neighbor in self.list_adjacency[predecessor]:
            if neighbor.name == successor:
                return True
        return False

    def thers_edge_adjacency(self, ed1: str, ed2: str):
        edge_name = str(ed1)
        edge2_name = str(ed2)

        if edge_name not in self.edges_map or edge2_name not in self.edges_map:
            raise ValueError("edges does not exist")

        nodes_ed1 = self.edges_map[edge_name]
        nodes_ed2 = self.edges_map[edge2_name]

        return any(v in nodes_ed2[:2] for v in nodes_ed1[:2])

    def is_complete(self):

        for node_key in self.list_adjacency:
            aux = self.list_adjacency[node_key]

            for key in self.nodes_map:

                if aux.count(self.nodes_map[key]) == 0 and node_key != key:
                    return False

        return True

    def is_simple(self):
        for node_key in self.list_adjacency:
            aux = self.list_adjacency[node_key]

            if aux.count(self.nodes_map[node_key]) > 0:
                return False
        return True
