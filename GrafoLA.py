from typing import Dict, List, Tuple
from models.DFSNode import DFSNode
from models.ExcludedEdge import ExcludedEdge
from models.NodeLA import NodeLA
import copy
import xmltodict


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

    def __str__(self):
        result = " List Adjacency\n"
        for node in self.list_adjacency:
            result += f"{node} -> "
            for neighbor in self.list_adjacency[node]:
                result += f"[{neighbor.name}] -> "
            result += "\n"
        return result

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

    # region Node Section
    def add_node(self, name: str, weight: float = 0):
        """
        Adds a new node to the graph.

        Parameters:
        name (str): The name of the node to be added.
        weight (float): The weight of the node to be added.

        Raises:
        ValueError: If a node with the given name already exists in the graph.
        """
        if name not in self.nodes_map:
            name = str(name)
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
            self.remove_all_edge_by_node(name)
            self.nodes_map.pop(name)
            self.list_adjacency.pop(name)
            for node in self.list_adjacency:
                self.list_adjacency[node] = list(
                    filter(lambda x: x.name != name, self.list_adjacency[node])
                )
        else:
            raise ValueError("NodeLA name not found")

    def thers_node_adjacency(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.list_adjacency or v2 not in self.list_adjacency:
            raise ValueError("nodes does not exist")

        for neighbor in self.list_adjacency[predecessor]:
            if neighbor.name == successor:
                return True
        return False

    def get_all_nodes_degree(self):
        nodes_degree: Dict[str, int] = {}
        for node_name in self.nodes_map.keys():
            nodes_degree[node_name] = 0
            size = len(self.list_adjacency)
            for edge in self.edges_map.values():
                if node_name in edge[:2]:
                    nodes_degree[node_name] += 1
        return nodes_degree

    # endregion
    # region Edge Section
    def add_edge(
        self, predecessor: str, successor: str, weight: float, name: str = None
    ):
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
        predecessor = str(predecessor)
        successor = str(successor)

        if predecessor not in self.list_adjacency:
            self.add_node(predecessor, None)
        if successor not in self.list_adjacency:
            self.add_node(successor, None)

        if name in self.edges_map:
            raise ValueError("Edge already exist")

        new_edge_name = len(self.edges_map) + 1

        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            new_edge_name += 1

        name = str(name)
        self.list_adjacency[predecessor].append(self.nodes_map[successor])

        if not self.DIRECTED and predecessor != successor:
            self.list_adjacency[successor].append(self.nodes_map[predecessor])

        self.edges_map[name] = (predecessor, successor, weight)

    def remove_edge_by_name(self, name: str):
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

    def remove_all_edge_by_node(self, node_name: str):
        """
        Removes all edges associated with a node from the graph.

        Args:
            node_name (str): The name of the node whose edges will be removed.

        This method removes all edges that are adjacent to the specified node from the graph.
        """
        for key in list(self.edges_map.keys()):
            v1, v2, _ = self.edges_map[key]
            if v1 == node_name or v2 == node_name:
                self.remove_edge_by_name(key)

    def remove_all_edge_by_nodes(self, predecessor: str, successor: str):
        """
        Removes all edges between two nodes from the graph.

        Args:
            predecessor (str): The name of the predecessor node.
            successor (str): The name of the successor node.

        This method removes all edges between the predecessor and successor nodes from the graph.
        """
        for key in list(self.edges_map.keys()):
            v1, v2, _ = self.edges_map[
                key
            ]  # _ is the weight of the edge that we are not using
            if v1 == predecessor and v2 == successor:
                self.remove_edge(key)

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

    def thers_edge_adjacency(self, ed1: str, ed2: str):
        edge_name = str(ed1)
        edge2_name = str(ed2)

        if edge_name not in self.edges_map or edge2_name not in self.edges_map:
            raise ValueError("edges does not exist")

        nodes_ed1 = self.edges_map[edge_name]
        nodes_ed2 = self.edges_map[edge2_name]

        return any(v in nodes_ed2[:2] for v in nodes_ed1[:2])

    def get_edges_by_node(self, node_name: str):
        """
        Get all edges that are adjacent to a node.

        Args:
            node_name (str): The name of the node.

        Returns:
            List[str]: A list with the names of the edges adjacent to the node.
        """
        node_name = str(node_name)
        edges = []
        for key in self.edges_map:
            v1, v2, _ = self.edges_map[key]
            if (v1 == node_name or v2 == node_name) and not self.DIRECTED:
                edges.append(key)
            elif v1 == node_name:
                edges.append(key)
        return edges

    # endregion
    # region Graph Section
    def is_empty(self):
        return len(self.list_adjacency) == 0

    def get_edge_count(self):
        return len(self.edges_map)

    def get_node_count(self):
        return len(self.list_adjacency)

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

    def is_connected(self):
        """
        Check if the graph is connected.
        Returns:
            bool: True if the graph is connected, False otherwise.
        """
        if self.is_empty():
            return True

        if self.DIRECTED:
            graph = self.make_underlying_graph()
            return graph.is_connected()

        time = [0]
        result: Dict[str, DFSNode] = {}

        for node_name in self.nodes_map.keys():
            result[str(node_name)] = DFSNode(0, 0, None)

        first_node = next(iter(self.nodes_map))
        self._dfs(first_node, time, result)

        return time[0] == len(self.nodes_map) * 2

    def _dfs(self, node_name, time, result):
        node_name = str(node_name)
        time[0] += 1
        result[node_name].discovery_time = time[0]

        for neighbor in self.list_adjacency[node_name]:

            if result[neighbor.name].discovery_time == 0:
                result[neighbor.name].parent = node_name
                self._dfs(neighbor.name, time, result)

        time[0] += 1
        result[node_name].finishing_time = time[0]

    def get_euler_path(self):
        """
        Get the Euler Path of the graph.
        Returns:
            List[str]: A list with the nodes name of the Euler Path.
        """
        if self.is_empty():
            return []

        if not self.is_connected():
            return []

        if not self.is_simple():
            raise ValueError("Graph is not simple")

        if self.DIRECTED:
            raise ValueError("Graph is directed")

        euler_path: List[str] = []
        copy_graph = copy.deepcopy(self)

        nodes_degree = copy_graph.get_all_nodes_degree()
        odd_degree_nodes = [
            node for node, degree in nodes_degree.items() if degree % 2 != 0
        ]

        if len(odd_degree_nodes) >= 3:
            return []

        current_node = (
            odd_degree_nodes[0] if odd_degree_nodes else next(iter(self.nodes_map))
        )

        while copy_graph.get_edge_count() > 0:
            euler_path.append(current_node)
            edges_of_current_node = copy_graph.get_edges_by_node(current_node)

            if len(edges_of_current_node) == 1:
                chosen_edge = edges_of_current_node[0]
            else:
                for edge_name in edges_of_current_node:
                    if not copy_graph.is_bridget(edge_name):
                        chosen_edge = edge_name
                        break

            v1, v2, _ = copy_graph.edges_map[chosen_edge]
            copy_graph.remove_edge_by_name(chosen_edge)
            current_node = v2 if v1 == current_node else v1

        if copy_graph.get_edge_count() != 0:
            raise ValueError("Graph has more than one connected component")

        return euler_path

    # endregion
    # region Bridge and Articulation Section
    def get_bridge(self):
        """
        Get all bridge edges in the graph.
        Returns:
            List[Edges]: A list with all bridge edges name.
        """
        if self.is_empty():
            return []

        bridges: List[str] = []
        copy_graph = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )

        for edge_name, edge_nodes in self.edges_map.items():
            copy_graph.remove_edge_by_name(edge_name)
            if not copy_graph.is_connected():
                bridges.append(edge_name)
            copy_graph.add_edge(edge_nodes[0], edge_nodes[1], 1, edge_name)

        return bridges

    def is_bridget(self, edge_name: str):
        """
        Check if the given edge is a bridge.
        Args:
            edge_name (str): The edge name.
        Returns:
            bool: True if the edge is a bridge, False otherwise.
        """
        edge_name = str(edge_name)

        if edge_name not in self.edges_map:
            raise ValueError("Edge name does not exist")

        copy_graph = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )
        copy_graph.remove_edge_by_name(edge_name)

        is_bridge = not copy_graph.is_connected()

        return is_bridge

    def get_articulations(self):

        if self.is_empty():
            return []

        articulations: List[str] = []
        excluded_edges: List[ExcludedEdge] = []

        copy_graph = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )

        for node_name in self.nodes_map.keys():
            excluded_edges = copy_graph._get_excluded_edges_by_node(node_name)
            copy_graph.remove_node(node_name)

            if not copy_graph.is_connected():
                articulations.append(node_name)

            copy_graph.add_node(node_name)
            for excluded_edge in excluded_edges:
                copy_graph.add_edge(
                    excluded_edge.v1, excluded_edge.v2, 1, excluded_edge.name
                )

        return articulations

    def is_articulation(self, node_name: str):
        """
        Check if the given node is an articulation.
        Args:
            node_name (str): The node name.
        Returns:
            bool: True if the node is an articulation, False otherwise.
        """
        node_name = str(node_name)

        if node_name not in self.nodes_map:
            raise ValueError("Node name does not exist")

        copy_graph = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )
        copy_graph.remove_node(node_name)

        is_articulation = not copy_graph.is_connected()

        return is_articulation

    def _get_excluded_edges_by_node(self, node: str):
        node = str(node)
        edges_name = [key for key in self.edges_map if node in self.edges_map[key]]
        excluded_edges = []
        for name in edges_name:
            excluded = ExcludedEdge(
                name, self.edges_map[name][0], self.edges_map[name][1]
            )
            excluded_edges.append(excluded)

        return excluded_edges

    # endregion
    # region Underlying Graph Section
    def make_underlying_graph(self):

        if not self.DIRECTED:
            raise ValueError("Graph is not directed")

        new_graph = GrafoLA(False)
        size = len(self.list_adjacency)

        for node in self.nodes_map.values():
            new_graph.add_node(node.name, node.weight)

        for edge_name in self.edges_map:
            predecessor, successor, weight = self.edges_map[edge_name]
            new_graph.add_edge(predecessor, successor, weight, edge_name)

        return new_graph

    def print_underlying_graph(self):
        aux = self.make_underlying_graph()
        print("Underlying Graph")
        print(str(aux))

    # endregion
    # region xml to graph Section
    def to_graph(self, path: str):

        with open(path, "rb") as file:
            xml = xmltodict.parse(file)

        nodes = xml["gexf"]["graph"]["nodes"]["node"]
        edges = xml["gexf"]["graph"]["edges"]["edge"]
        self.DIRECTED = xml["gexf"]["graph"]["@defaultedgetype"] == "directed"

        for node in nodes:
            self.add_node(node["@label"], node["attvalues"]["attvalue"]["@value"])

        if edges == None:
            return self
        print(len(edges))
        if len(edges) == 4 and edges["@source"] != None:
            edges = [edges]

        for edge in edges:
            for node in nodes:
                if (edge["@source"]) == node["@id"]:
                    source = node["@label"]
                if edge["@target"] == node["@id"]:
                    target = node["@label"]

            self.add_edge(source, target, edge["@weight"], edge["@label"])
        return self

    # endregion
    # region XML Section

    def to_xml(self):
        result = '<?xml version="1.0" encoding="UTF-8"?>\n'
        result += '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd" version="1.3">\n'
        result += f"<graph defaultedgetype=\"{'directed' if self.DIRECTED else 'undirected'}\">\n"
        result += self.__writeGraph()
        result += "</graph>\n"
        result += "</gexf>\n"

        open("output/graphLA.gexf", "w").write(result)

    def __writeGraph(self):
        result = '<attributes class="node">\n'
        result += '<attribute id="0" title="weight" type="float"/>\n'
        result += "</attributes>\n"
        result += "<nodes>\n"
        for node in self.nodes_map.values():
            result += self.__writeNode(node)
        result += "</nodes>\n"
        result += "<edges>\n"
        for name in self.edges_map:

            result += self.__writeEdge(name)
        result += "</edges>\n"
        return result

    def __writeNode(self, node: NodeLA):
        result = f'<node id="{node.name}" label="{node.name}">\n'
        result += "<attvalues>\n"
        result += '<attvalue for="0" value="' + str(node.weight) + '"/>\n'
        result += "</attvalues>\n"
        result += "</node>\n"

        return result

    def __writeEdge(self, edge: str):

        predecessor, successor, weight = self.edges_map[edge]
        result = f"<edge label='{edge}' source='{predecessor}' target='{successor}' weight='{weight}'/>\n"

        return result

    # endregion
