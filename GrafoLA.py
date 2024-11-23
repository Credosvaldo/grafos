from multiprocessing import Process
from typing import Dict, List, Tuple
from models.TarjansNode import TarjansNode
from models.DFSNode import DFSNode
from models.ExcludedEdge import ExcludedEdge
from models.NodeLA import NodeLA
from enums.ConnectivityDegree import ConnectivityDegree
import copy
import xmltodict


class GrafoLA:

    def __init__(
        self,
        DIRECTED: bool = True,
        num_nodes: int = 0,
        nodes: List[Tuple[str, float]] = [],
        edges: List[Tuple[str, str, float]] = [],
    ):

        self.nodes_map: Dict[str, NodeLA] = {}
        self.edges_map: Dict[str, Tuple[str, str, float]] = (
            {}
        )  # predecessor , successor, weight
        self.DIRECTED = DIRECTED
        self.list_adjacency: Dict[str, List[NodeLA]] = {}
        self.create_adjacency_list(num_nodes, nodes, edges)

    def __str__(self) -> str:
        result = " List Adjacency\n"
        for node in self.list_adjacency:
            result += f"{node} -> "
            for neighbor in self.list_adjacency[node]:
                for key in self.edges_map:
                    predecessor, successor, weight = self.edges_map[key]
                    if predecessor == node and successor == neighbor.name:
                        result += f"[{neighbor.name } ({weight})] -> "
                        break
                    elif not self.DIRECTED and predecessor == neighbor.name:
                        result += f"[{neighbor.name } ({weight})] -> "
                        break

            result += "\n"
        return result

    def create_adjacency_list(
        self,
        num_nodes: int,
        nodes: List[Tuple[str, float]] = [],
        edges: List[Tuple[str, str, float]] = [],
    ):
        if nodes == [] and num_nodes == 0:
            return {}

        if len(nodes) != num_nodes and nodes != []:
            raise ValueError(
                "Number of nodes does not match the number of nodes provided"
            )

        for i in range(num_nodes):

            name = None if nodes == [] else nodes[i][0]
            weight = None if nodes == [] else nodes[i][1]
            new_edge_name = len(self.edges_map) + 1

            while name is None or name in self.nodes_map:
                name = str(new_edge_name)
                new_edge_name += 1

            name = str(name)
            self.add_node(name, weight)

        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

    # region Node Section
    def add_node(self, name: str, weight: float = 1.0):
        """
        Adds a new node to the graph.

        Parameters:
        name (str): The name of the node to be added.
        weight (float): The weight of the node to be added.

        Raises:
        ValueError: If a node with the given name already exists in the graph.
        """
        name = str(name)
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
        name = str(name)
        if name in self.nodes_map:
            self.remove_all_edges_by_node(name)
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
    
    def thers_only_one_edge_btwn_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.list_adjacency or v2 not in self.list_adjacency:
            raise ValueError("nodes does not exist")

        thers_edge = False
        for neighbor in self.list_adjacency[predecessor]:
            if neighbor.name != successor:
                continue
            
            if thers_edge:
                return False
            else:
                thers_edge = True
                
        return thers_edge

    def get_all_nodes_degree(self):
        nodes_degree: Dict[str, int] = {}
        for node_name in self.nodes_map.keys():
            nodes_degree[node_name] = len(self.list_adjacency[node_name])

        return nodes_degree

    # endregion
    # region Edge Section
    def add_edge(
        self, predecessor: str, successor: str, weight: float = 1, name: str = None
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
            self.add_node(predecessor)
        if successor not in self.list_adjacency:
            self.add_node(successor)

        if name in self.edges_map:
            raise ValueError("Edge already exist")

        new_edge_name = len(self.edges_map) + 1

        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            new_edge_name += 1

        name = str(name)
        self.list_adjacency[predecessor].append(self.nodes_map[successor])

        if not self.DIRECTED:
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

    def remove_all_edges_by_node(self, node_name: str):
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

    def remove_all_edges_by_nodes(self, predecessor: str, successor: str):
        """
        Removes all edges between two nodes from the graph.

        Args:
            predecessor (str): The name of the predecessor node.
            successor (str): The name of the successor node.

        This method removes all edges between the predecessor and successor nodes from the graph.
        """
        predecessor = str(predecessor)
        successor = str(successor)
        for key in list(self.edges_map.keys()):
            v1, v2, _ = self.edges_map[
                key
            ]  # _ is the weight of the edge that we are not using
            if v1 == predecessor and v2 == successor:
                self.remove_edge_by_name(key)

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

    def thers_edge_adjacency(self, edge1: str, edge2: str):
        edge_name = str(edge1)
        edge2_name = str(edge2)

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

    def get_edge_by_nodes(self, predecessor: str, successor: str):
        """
        Get the edge between two nodes.

        Args:
            predecessor (str): The name of the predecessor node.
            successor (str): The name of the successor node.

        Returns:
            str: The name of the edge between the two nodes.
        """
        predecessor = str(predecessor)
        successor = str(successor)
        for key in self.edges_map:
            v1, v2, _ = self.edges_map[key]
            if v1 == predecessor and v2 == successor:
                return key
        return None

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
            for key in self.nodes_map:
                if node_key == key and self.thers_node_adjacency(node_key, key):
                    return False
                if node_key != key and not self.thers_only_one_edge_btwn_nodes(node_key, key):
                    return False

        return True

    def is_simple(self):
        for node_key in self.list_adjacency:
            aux = self.list_adjacency[node_key]

            if aux.count(self.nodes_map[node_key]) > 0:
                return False

            for neighbor in aux:
                if aux.count(neighbor) > 1:
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

    def get_euler_path(self, by_tarjan: bool = True):
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
        is_bridge_method = copy_graph.is_bridge_by_tarjan if by_tarjan else copy_graph.is_bridge

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
            last_edge = False

            if len(edges_of_current_node) == 1:
                chosen_edge = edges_of_current_node[0]
                last_edge = True
            else:
                for edge_name in edges_of_current_node:
                    if not is_bridge_method(edge_name):
                        chosen_edge = edge_name
                        last_edge = False
                        break

            v1, v2, _ = copy_graph.edges_map[chosen_edge]
            current_node = v2 if v1 == current_node else v1

            if last_edge:
                copy_graph.remove_node(current_node)
            else:
                copy_graph.remove_edge_by_name(chosen_edge)

        if copy_graph.get_edge_count() != 0:
            raise ValueError("Graph has more than one connected component")

        euler_path.append(current_node)
        return euler_path

    def _depth_first_search(self, graph: "GrafoLA" = None):

        time = [0]
        result: Dict[str, DFSNode] = {}

        for node_name in self.nodes_map.keys():
            result[node_name] = DFSNode(0, 0, None)

        for node_name, node_value in result.items():
            if node_value.discovery_time == 0:
                self._dfs(node_name, time, result)

        return result

    def make_revert_graph(self):

        if not self.DIRECTED:
            raise ValueError("Graph is not directed")

        new_graph = GrafoLA(True)

        for node_name in self.nodes_map.keys():
            node = self.nodes_map[node_name]
            new_graph.add_node(node.name, node.weight)

        for edge_name in self.edges_map.keys():
            predecessor, successor, weight = self.edges_map[edge_name]
            new_graph.add_edge(successor, predecessor, weight, edge_name)

        return new_graph

    def print_revert_graph(self):
        aux = self.make_revert_graph()
        print("Revert Graph")
        print(aux)

    def kosaraju(self):
        if not self.DIRECTED:
            raise ValueError("Graph is not directed")

        number_of_strongly_connected_components = 0
        dfs = self._depth_first_search()
        revert = self.make_revert_graph()

        sorted_keys = sorted(
            dfs.keys(), reverse=True, key=lambda k: dfs[k].finishing_time
        )

        time = [0]
        result = self._get_dfs_result_structure(sorted_keys)

        for key in sorted_keys:
            if result[key].discovery_time == 0:
                revert._dfs(key, time, result)

        for dfs_node in result.values():
            if dfs_node.parent == None:
                number_of_strongly_connected_components += 1

        return number_of_strongly_connected_components

    # endregion
    # region Bridge and Articulation Section
    def get_bridge(self):
        """
        Get all bridge edges in the graph.
        Returns:
            List[Edges]: A list with all bridge edges name.
        """
        if not self.is_connected():
            raise ValueError("Graph is not connected")

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

    def is_bridge(self, edge_name: str):
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
        v1, v2, _ = self.edges_map[edge_name]

        is_bridge = not copy_graph.reachable(v1, v2)

        return is_bridge

    def get_articulations(self):
        if not self.is_connected():
            raise ValueError("Graph is not connected")

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

        graph = xml["gexf"]["graph"]
        nodes = graph["nodes"]["node"]
        edges = graph["edges"]

        self.DIRECTED = graph["@defaultedgetype"] == "directed"

        for node in nodes:
            self.add_node(node["@label"], node["attvalues"]["attvalue"]["@value"])

        if edges == None:
            return self
        else:
            edges = edges["edge"]

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

    def _get_dfs_result_structure(self, nodes_group: List[str] = None):
        if nodes_group == None:
            nodes_group = self.nodes_map.keys()

        result: Dict[str, DFSNode] = {}
        for node_name in nodes_group:
            result[node_name] = DFSNode(0, 0, None)
        return result

    def connectivity_degree(self):
        if not self.is_connected():
            return ConnectivityDegree.DISCONNECTED

        if self.kosaraju() == 1:
            return ConnectivityDegree.STRONGLY_CONNECTED

        results: Dict[str, Dict[str, DFSNode]] = {}

        for v1_name in self.nodes_map.keys():
            for v2_name in self.nodes_map.keys():
                if v1_name != v2_name:
                    v1_to_v2 = self.reachable(v1_name, v2_name, results)
                    v2_to_v1 = self.reachable(v2_name, v1_name, results)
                    if not (v1_to_v2 or v2_to_v1):
                        return ConnectivityDegree.WEAKLY_CONNECTED

        return ConnectivityDegree.UNIDIRECTIONAL_CONNECTED

    def reachable(self, v1: str, v2: str, results: Dict[str, Dict[str, DFSNode]] = {}):
        v1 = str(v1)
        v2 = str(v2)

        if v1 not in results.keys():
            result = self._get_dfs_result_structure()
            self._dfs(v1, [0], result)
            results[v1] = result

        return results[v1][v2].discovery_time != 0

    def _tarjan_dfs(
        self,
        node_name: str,
        result: Dict[str, TarjansNode],
        bridges: List[str],
        time: List[int],
    ):
        result[node_name].visited = True
        result[node_name].disc = time[0]
        result[node_name].low = time[0]
        time[0] += 1

        for v in self.list_adjacency[node_name]:
            if not result[v.name].visited:
                result[v.name].parent = node_name

                self._tarjan_dfs(v.name, result, bridges, time)

                result[node_name].low = min(result[node_name].low, result[v.name].low)

                if result[v.name].low > result[node_name].disc:
                    bridges.append(self.get_edge_by_nodes(node_name, v.name))

            elif v.name != result[node_name].parent:
                result[node_name].low = min(result[node_name].low, result[v.name].disc)

    def get_bridge_by_tarjan(self):
        if not self.is_connected():
            raise ValueError("Graph is not connected")

        if self.is_empty():
            return []

        time = [0]
        bridges: List[str] = []
        copy_graph = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )

        result: Dict[str, TarjansNode] = {}

        for node_name in self.nodes_map.keys():
            result[node_name] = TarjansNode(False, None, 0, 0)

        for node_name in copy_graph.nodes_map.keys():
            if not result[node_name].visited:
                self._tarjan_dfs(node_name, result, bridges, time)

        return bridges
    
    def is_bridge_by_tarjan(self, edge_name: str):
        edge_name = str(edge_name)
        bridges = self.get_bridge_by_tarjan()
        return edge_name in bridges

    # endregion
