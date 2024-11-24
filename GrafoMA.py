from multiprocessing import Process, Manager
import random
from typing import Dict, List, Tuple
from IGrafo import IGrafo
from enums.ConnectivityDegree import ConnectivityDegree
from models.TarjansNode import TarjansNode
from models.DFSNode import DFSNode
from models.Edge import Edge
from models.ExcludedEdge import ExcludedEdge
from models.Node import Node
from datetime import datetime
import copy
import xmltodict


class GrafoMA(IGrafo):

    def __init__(
        self,
        DIRECTED: bool = True,
        num_nodes: int = 0,
        nodes: List[Tuple[str, float]] = [],
        random_graph_generation: bool = False,
    ):
        self.matrix_adjacency: List[List[List[Edge]]] = self._create_matrix(num_nodes)
        self.nodes_map: Dict[str, Node] = {}
        self.edges_map: Dict[str, Tuple[str, str, int]] = {}
        self.DIRECTED = DIRECTED
        self.excluded_nodes_index = []
        self._fill_nodes_map(num_nodes, nodes, random_graph_generation)

    def matrix(self):
        result = "   Adjacency Matrix\n\n"
        result += "      "
        for i in range(len(self.nodes_map)):
            headers = f"{list(self.nodes_map.keys())[i]:<5}"
            result += headers
        result += "\n"

        for i in range(len(self.matrix_adjacency)):
            row = f"{list(self.nodes_map.keys())[i]:<2}| "
            for j in range(len(self.matrix_adjacency)):
                cell = self.matrix_adjacency[i][j]
                if cell.__len__() == 0:
                    row += "  0  "
                elif cell.__len__() == 1:
                    row += "  1  "
                else:
                    row += f"  {cell.__len__():<3}"
            result += row + "\n"
        return result

    def weight_matrix(self):
        result = "   Weight Matrix\n\n"
        result += "      "
        for i in range(len(self.nodes_map)):
            headers = f"{list(self.nodes_map.keys())[i]:<5}"
            result += headers
        result += "\n"

        for i in range(len(self.matrix_adjacency)):
            row = f"{list(self.nodes_map.keys())[i]:<2}| "
            for j in range(len(self.matrix_adjacency)):
                cell = self.matrix_adjacency[i][j]
                if cell.__len__() == 0:
                    row += "  -  "
                elif cell.__len__() == 1:
                    row += f"  {cell[0].weight:<3}"
                else:
                    for edge in cell:
                        row += f" {edge.weight} "
            result += row + "\n"
        return result

    def __str__(self):  # this functions was __str__ before
        string = "[\n  "
        string += "\n  ".join(
            str(row)
            for i, row in enumerate(self.matrix_adjacency)
            if i not in self.excluded_nodes_index
        )
        string += "\n]"
        return string

    def add_edge(
        self, predecessor: str, successor: str, weight: float = 1, name: str = None
    ):
        if name != None and str(name) in self.edges_map:
            raise ValueError("Edge name already exists")

        new_edge_name = len(self.edges_map) + 1

        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            new_edge_name += 1

        name = str(name)

        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map:
            self.add_node(v1)

        if v2 not in self.nodes_map:
            self.add_node(v2)

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        new_edge_parallel_index = len(self.matrix_adjacency[v1_index][v2_index])

        self.matrix_adjacency[v1_index][v2_index].append(Edge(name, weight))
        self.edges_map[name] = (v1, v2, new_edge_parallel_index)

        if not self.DIRECTED and v1_index != v2_index:
            self.matrix_adjacency[v2_index][v1_index].append(Edge(name, weight))

    def remove_edge_by_name(self, name: str):
        name = str(name)

        if name not in self.edges_map:
            raise ValueError("Edge name does not exist")

        v1, v2, parallel_index = self.edges_map[name]
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        for edge in self.matrix_adjacency[v1_index][v2_index][parallel_index + 1 :]:
            temp_list = list(self.edges_map[edge.name])
            temp_list[2] -= 1
            self.edges_map[edge.name] = tuple(temp_list)

        self.matrix_adjacency[v1_index][v2_index].pop(parallel_index)
        del self.edges_map[name]

        if not self.DIRECTED and v1_index != v2_index:
            self.matrix_adjacency[v2_index][v1_index].pop(parallel_index)

    # Remove all edges between two nodes
    def remove_all_edges_by_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Nodes does not exist")

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        for edge in self.matrix_adjacency[v1_index][v2_index]:
            self.edges_map.pop(edge.name)
        self.matrix_adjacency[v1_index][v2_index] = []

        if self.DIRECTED:
            for edge in self.matrix_adjacency[v2_index][v1_index]:
                self.edges_map.pop(edge.name)
            self.matrix_adjacency[v2_index][v1_index] = []

    def add_node(self, name: str = None, weight: float = 1.0):
        if str(name) in self.nodes_map:
            raise ValueError("Node already exists")

        matrix_size = len(self.matrix_adjacency)
        node_name_index = matrix_size
        new_size = matrix_size + 1

        if self.excluded_nodes_index:
            new_node_index = self.excluded_nodes_index.pop(0)
            usin_a_excluded_node = True
        else:
            new_node_index = matrix_size
            usin_a_excluded_node = False

        while name is None or name in self.nodes_map:
            name = str(node_name_index)
            node_name_index += 1

        name = str(name)
        self.nodes_map[name] = Node(new_node_index, weight)

        if usin_a_excluded_node:
            return

        self.matrix_adjacency.append([[] for _ in range(new_size)])
        for i in range(matrix_size):
            self.matrix_adjacency[i].append([])

    def remove_node(self, name: str):
        name = str(name)

        if name not in self.nodes_map:
            raise ValueError("node does not exist")

        size = len(self.matrix_adjacency)
        node_index = self.nodes_map[name].index
        self.excluded_nodes_index.append(node_index)

        for i in range(size):
            for edge in self.matrix_adjacency[i][node_index]:
                del self.edges_map[edge.name]

            if self.DIRECTED:
                for edge in self.matrix_adjacency[node_index][i]:
                    del self.edges_map[edge.name]

            self.matrix_adjacency[i][node_index] = []
            self.matrix_adjacency[node_index][i] = []

        self.nodes_map.pop(name)

    def thers_node_adjacency(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("nodes does not exist")

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        return self.matrix_adjacency[v1_index][v2_index] != []

    def thers_edge_adjacency(self, edge1: str, edge2: str):
        edge1 = str(edge1)
        edge2 = str(edge2)

        nodes_ed1 = self.edges_map[edge1]
        nodes_ed2 = self.edges_map[edge2]

        return any(v in nodes_ed2[:2] for v in nodes_ed1[:2])

    def thers_edge_by_name(self, name: str):
        name = str(name)
        return name in self.edges_map

    def thers_edge_by_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        return self.matrix_adjacency[v1_index][v2_index] != []

    def thers_only_one_edge_btwn_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        return len(self.matrix_adjacency[v1_index][v2_index]) == 1

    def get_edge_count(self):
        return len(self.edges_map)

    def get_node_count(self):
        return len(self.nodes_map)

    def is_empty(self):
        return len(self.matrix_adjacency) - len(self.excluded_nodes_index) == 0

    def is_complete(self):
        for v1_name in self.nodes_map.keys():
            for v2_name in self.nodes_map.keys():
                if v1_name == v2_name and self.thers_edge_by_nodes(v1_name, v2_name):
                    return False
                if v1_name != v2_name and not self.thers_only_one_edge_btwn_nodes(
                    v1_name, v2_name
                ):
                    return False

        return True

    def is_simple(self):
        size = len(self.matrix_adjacency)
        for i in range(size):
            for j in range(size):
                if i != j and len(self.matrix_adjacency[i][j]) > 1:
                    return False
                if i == j and len(self.matrix_adjacency[i][j]) != 0:
                    return False
        return True

    def _create_matrix(self, rows, cols=None):
        if cols is None:
            cols = rows
        return [[[] for _ in range(cols)] for _ in range(rows)]

    def _generate_node_name(self, index: int) -> str:
        resultado = ""
        while index >= 0:
            resultado = chr(index % 26 + ord("A")) + resultado
            index = index // 26 - 1
        return resultado

    def _fill_nodes_map(
        self,
        num_nodes: int,
        nodes: List[Tuple[str, float]],
        random_graph_generation: bool = False,
    ):
        if not nodes:
            for i in range(num_nodes):
                self.nodes_map[str(i + 1)] = Node(i)
            if random_graph_generation:
                self._create_random_edges()

        elif num_nodes == 0 or len(nodes) == num_nodes:
            self.matrix_adjacency = self._create_matrix(len(nodes))
            for i in range(len(nodes)):
                node_name = str(nodes[i][0])
                node_weight = float(nodes[i][1])

                self.nodes_map[node_name] = Node(i, node_weight)
        else:
            raise ValueError("Number of nodes and nodes list does not match")

    def make_revert_graph(self):
        """
        Creates a new graph with all edges reversed from the original graph.
        Raises:
            ValueError: If the graph is not directed.
        Returns:
            GraphMatrixAdjacency: A new graph instance with reversed edges.
        """

        if not self.DIRECTED:
            raise ValueError("Graph is not directed")

        new_graph = GrafoMA(True)
        size = len(self.matrix_adjacency)

        for name, node in self.nodes_map.items():
            new_graph.add_node(name, node.weight)

        for i in range(size):
            for j in range(size):
                edge = self.matrix_adjacency[i][j]
                if edge.__len__() == 0:
                    continue
                for edge in edge:
                    new_graph.add_edge(
                        self.edges_map[edge.name][1],
                        self.edges_map[edge.name][0],
                        edge.weight,
                        edge.name,
                    )

        return new_graph

    def make_underlying_graph(self):

        if not self.DIRECTED:
            raise ValueError("Graph is not directed")

        new_graph = GrafoMA(False)
        size = len(self.matrix_adjacency)

        for name, node in self.nodes_map.items():
            new_graph.add_node(name, node.weight)

        for i in range(size):
            for j in range(size):
                edges = self.matrix_adjacency[i][j]
                if len(edges) == 0:
                    continue
                for edge in edges:
                    new_graph.add_edge(
                        self.edges_map[edge.name][0],
                        self.edges_map[edge.name][1],
                        edge.weight,
                        edge.name,
                    )

        return new_graph


    def _depth_first_search(self):

        time = [0]
        result = self._get_dfs_result_structure()

        for node_name, node_value in result.items():
            if node_value.discovery_time == 0:
                self._dfs(node_name, time, result)

        return result

    def _dfs(self, node_name, time, result):
        node_name = str(node_name)
        time[0] += 1
        result[node_name].discovery_time = time[0]
        size = len(self.matrix_adjacency)

        node_index = self.nodes_map[node_name].index

        for i in range(size):
            if self.matrix_adjacency[node_index][i]:
                edge_name = self.matrix_adjacency[node_index][i][0].name
                edge_nodes = self.edges_map[edge_name]
                successor_name = (
                    edge_nodes[1] if edge_nodes[1] != node_name else edge_nodes[0]
                )

                if result[successor_name].discovery_time == 0:
                    result[successor_name].parent = node_name
                    self._dfs(successor_name, time, result)

        time[0] += 1
        result[node_name].finishing_time = time[0]

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
        result = self._get_dfs_result_structure()

        first_node = next(iter(self.nodes_map))
        self._dfs(first_node, time, result)

        return time[0] == len(self.nodes_map) * 2

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

        v1, v2, _ = copy_graph.edges_map[edge_name]
        copy_graph.remove_edge_by_name(edge_name)

        is_bridge = not copy_graph.reachable(v1, v2)

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
        edges_name = [
            edge.name
            for sublist in self.matrix_adjacency[self.nodes_map[node].index]
            for edge in sublist
        ]
        excluded_edges = []
        for name in edges_name:
            excluded = ExcludedEdge(
                name, self.edges_map[name][0], self.edges_map[name][1]
            )
            excluded_edges.append(excluded)

        return excluded_edges

    def get_euler_path(self, by_tarjan: bool = True):
        """
        Get the euler path of the graph.
        Args:
            by_tarjan (bool): Use Tarjan algorithm to find the bridge edges.
        Returns:
            List[str]: A list with the euler path.
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
        is_bridge_method = (
            copy_graph.is_bridge_by_tarjan if by_tarjan else copy_graph.is_bridge
        )

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

    def get_edges_by_node(self, node_name: str):
        """
        Get all edges that are connected to the given node.
        Args:
            node (str): The node name.
        Returns:
            List[str]: A list with the edges name.
        """
        node_name = str(node_name)
        node_index = self.nodes_map[node_name].index
        edges_name = [
            edge.name
            for sublist in self.matrix_adjacency[node_index]
            for edge in sublist
        ]
        return edges_name

    def get_all_nodes_degree(self):
        nodes_degree: Dict[str, int] = {}
        for node_name in self.nodes_map.keys():
            nodes_degree[node_name] = 0
            node_index = self.nodes_map[node_name].index
            size = len(self.matrix_adjacency)
            for i in range(size):
                edges = self.matrix_adjacency[node_index][i]
                nodes_degree[node_name] += len(edges)
        return nodes_degree

    def __writeNode(self, node_name: str):
        node = self.nodes_map[node_name]
        result = f'<node id="{node_name}" label="{node_name}">\n'
        result += "<attvalues>\n"
        result += '<attvalue for="0" value="' + str(node.weight) + '"/>\n'
        result += "</attvalues>\n"
        result += "</node>\n"

        return result

    def __writeEdge(self, edge_name: str):

        predecessor_name, successor_name, index = self.edges_map[edge_name]
        predecessor_index = self.nodes_map[predecessor_name].index
        successor_index = self.nodes_map[successor_name].index
        weight = self.matrix_adjacency[predecessor_index][successor_index][index].weight

        result = f"<edge label='{edge_name}' source='{predecessor_name}' target='{successor_name}' weight='{weight}'/>\n"

        return result

    def __writeGraph(self):
        result = '<attributes class="node">\n'
        result += '<attribute id="0" title="weight" type="float"/>\n'
        result += "</attributes>\n"
        result += "<nodes>\n"
        for node in self.nodes_map:
            result += (
                self.__writeNode(node)
                if self.nodes_map[node].index not in self.excluded_nodes_index
                else ""
            )
        result += "</nodes>\n"
        result += "<edges>\n"
        for name in self.edges_map:

            result += self.__writeEdge(name)
        result += "</edges>\n"
        return result

    def to_xml(self):
        result = '<?xml version="1.0" encoding="UTF-8"?>\n'
        result += '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd" version="1.3">\n'
        result += f"<graph defaultedgetype=\"{'directed' if self.DIRECTED else 'undirected'}\">\n"
        result += self.__writeGraph()
        result += "</graph>\n"
        result += "</gexf>\n"

        with open("output/graphMA.gexf", "w") as file:
            file.write(result)

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

    def _paralel_dfs(self, shared_dict):
        result = self._depth_first_search()
        shared_dict["dfs"] = result

    def _paralel_make_revert_graph(self, shared_dict):
        result = self.make_revert_graph()
        shared_dict["revert"] = result

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

        node_index = self.nodes_map[node_name].index

        for v in self.matrix_adjacency[node_index]:
            if len(v) == 0:
                continue

            edge = v[0]
            v1, v2, _ = self.edges_map[edge.name]
            neibor = v2 if v1 == node_name else v1

            if not result[neibor].visited:
                result[neibor].parent = node_name

                self._tarjan_dfs(neibor, result, bridges, time)

                result[node_name].low = min(result[node_name].low, result[neibor].low)

                if result[neibor].low > result[node_name].disc:
                    bridges.append(edge.name)

            elif neibor != result[node_name].parent:
                result[node_name].low = min(result[node_name].low, result[neibor].disc)

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

    def _get_dfs_result_structure(self, nodes_group: List[str] = None):
        if nodes_group == None:
            nodes_group = self.nodes_map.keys()

        result: Dict[str, DFSNode] = {}
        for node_name in nodes_group:
            result[node_name] = DFSNode(0, 0, None)
        return result

    def is_bridge_by_tarjan(self, edge_name: str):
        edge_name = str(edge_name)
        bridges = self.get_bridge_by_tarjan()
        return edge_name in bridges

    def _create_random_edges(self):
        for v1_name in self.nodes_map.keys():
            for v2_name in self.nodes_map.keys():
                should_add_edge = random.randint(1, 5) == 1
                v1_index = self.nodes_map[v1_name].index
                v2_index = self.nodes_map[v2_name].index

                if v1_index < v2_index and should_add_edge:
                    self.add_edge(v1_name, v2_name, 1)
                    
                if v2_index == (len(self.matrix_adjacency) - 1):
                    if self.get_edges_by_node(v1_name) == []:
                        self.add_edge(v1_name, random.randint(1, v2_index+1), 1)
