from typing import Dict, List, Tuple
from Edge import Edge
from Node import Node

class GrafoMA:
    
    def __init__(self, DIRECTED: bool = True, num_nodes: int = 0, nodes: List[Tuple[str, float]] = []):
        self.matrix_adjacency = self._create_matrix(num_nodes)
        self.nodes_map: Dict[str, Node] = {}
        self.edges_map: Dict[str, Tuple[str, str, int]] = {}
        self.DIRECTED = DIRECTED
        self.excluded_nodes_index = []
        self._fill_nodes_map(num_nodes, nodes)
        
    def __str__(self):
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
    
    def print_weight_matrix(self):
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
        print(result)
        
    def show_some(self): # this functions was __str__ before
        string = '[\n  '
        string += '\n  '.join(str(row) for i, row in enumerate(self.matrix_adjacency) if i not in self.excluded_nodes_index)
        string += '\n]'
        return string
    
    def add_edge(self, predecessor: str, successor: str, weight: float = 1, name: str = None):
        if name != None and str(name) in self.edges_map:
            raise ValueError("Edge name already exists")
        
        new_edge_name = len(self.edges_map) + 1
        
        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            new_edge_name += 1
            
        name = str(name)

        v1 = str(predecessor)
        v2 = str(successor)
        
        if(v1 not in self.nodes_map):
            self.add_node(v1)
        
        if(v2 not in self.nodes_map):
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
        
        self.matrix_adjacency[v1_index][v2_index].pop(parallel_index)
        del self.edges_map[name]
        
        if not self.DIRECTED and v1_index != v2_index:
            self.matrix_adjacency[v2_index][v1_index].pop(parallel_index)
        
    # Remove all edges between two nodes
    def remove_all_edge_by_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)
        
        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Nodes does not exist")
        
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        
        for edge in self.matrix_adjacency[v1_index][v2_index]:
            self.edges_map.pop(edge.name)
        self.matrix_adjacency[v1_index][v2_index] = []
        
        if not self.DIRECTED:
            for edge in self.matrix_adjacency[v2_index][v1_index]:
                self.edges_map.pop(edge.name)
            self.matrix_adjacency[v2_index][v1_index] = []
               
    def add_node(self, name: str = None, weight: float = 0):
        if str(name) in self.nodes_map:
            raise ValueError("Node already exists")      
        
        matrix_size = len(self.matrix_adjacency)
        node_name_index = matrix_size
        new_size = matrix_size + 1

        if self.excluded_nodes_index:
            new_node_index = self.excluded_nodes_index.pop(0)
            usin_a_excluded_node = True
        else:
            new_node_index = len(self.matrix_adjacency)
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
        
        node_index = self.nodes_map[name].index
        self.excluded_nodes_index.append(node_index)
        
        for i in range(len(self.matrix_adjacency)):
            for edge in self.matrix_adjacency[i][node_index]:
                del self.edges_map[edge.name]
                    
            if self.DIRECTED:
                for edge in self.matrix_adjacency[node_index][i]:
                    del self.edges_map[edge.name]
                    
            self.matrix_adjacency[i][node_index] = []
            self.matrix_adjacency[node_index][i] = []
        
        self.nodes_map.pop(name)
    
    def thers_node_adjacente(self, predecessor: str, successor: str):        
        v1 = str(predecessor)
        v2 = str(successor)
        
        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("nodes does not exist")
        
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        return self.matrix_adjacency[v1_index][v2_index] != []
    
    def thers_edge_adjacence(self, ed1: str, ed2: str):
        ed1 = str(ed1)
        ed2 = str(ed2)
        
        nodes_ed1 = self.edges_map[ed1]
        nodes_ed2 = self.edges_map[ed2]
        
        return any(v in nodes_ed2[:2] for v in nodes_ed1[:2])
        
    def thers_edge_by_name(self, name: str):
        name = str(name)
        return name in self.edges_map
    
    def thers_edge_by_nodes(self, predecessor: str, successor: str):
        v1 = str(v1)
        v2 = str(v2)
    
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        return self.matrix_adjacency[v1_index][v2_index] != []
        
    def get_edge_count(self):
        return len(self.edges_map)
    
    def get_node_count(self):
        return len(self.nodes_map)
    
    def is_empty(self):
        return len(self.matrix_adjacency) - len(self.excluded_nodes_index) == 0
    
    def is_complete(self):
        size = len(self.matrix_adjacency)
        for i in range(size):
            for j in range(size):
                if i != j and len(self.matrix_adjacency[i][j]) != 1:
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
            resultado = chr(index % 26 + ord('A')) + resultado
            index = index // 26 - 1
        return resultado

    def _fill_nodes_map(self, num_nodes, nodes):
        if not nodes:
            for i in range(num_nodes):
                self.nodes_map[i] = str(i+1)
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

        for node in self.nodes_map.keys():
            new_graph.add_node(node, self.nodes_map[node].weight)

        for i in range(len(self.matrix_adjacency)):
            for j in range(len(self.matrix_adjacency[i])):
                edge = self.matrix_adjacency[i][j]
                if edge.__len__() == 0:
                    continue
                for edge in edge:
                    new_graph.add_edge(
                        self.edges_map[edge.name][1], self.edges_map[edge.name][0], edge.weight, edge.name
                    )

        return new_graph
    
    def print_revert_graph(self):
        aux = self.make_revert_graph()
        print("Revert Graph")
        print(str(aux))

    def make_underlying_graph(self):

        if not self.DIRECTED:
            raise ValueError("Graph is not directed")

        new_graph = GrafoMA(False)
        for node in self.nodes_map.keys():
            new_graph.add_node(node, self.nodes_map[node].weight)

        for i in range(len(self.matrix_adjacency)):
            for j in range(len(self.matrix_adjacency[i])):
                edge = self.matrix_adjacency[i][j]
                if edge.__len__() == 0:
                    continue
                for edge in edge:
                    new_graph.add_edge(
                        self.edges_map[edge.name][0], self.edges_map[edge.name][1], edge.weight, edge.name
                    )

        return new_graph


    def print_underlying_graph(self):
        aux = self.make_underlying_graph()
        print("Underlying Graph")
        print(str(aux))