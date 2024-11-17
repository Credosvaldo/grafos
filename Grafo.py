from typing import Dict, List, Tuple
from Edge import Edge
from Node import Node

class GrafoMA:
    
    def __init__(self, DIRECTED: bool = True, num_vertices: int = 0, vertices: List[Tuple[str, float]] = []):
        self.matriz_adjacencia = self._create_matriz(num_vertices)
        self.vertices_map: Dict[str, Node] = {}
        self.edges_map: Dict[str, Tuple[str, str, int]] = {}
        self.DIRECTED = DIRECTED
        self._fill_vertices_map(num_vertices, vertices)
        
    def __str__(self) -> str:
        string = '[\n  '
        string += '\n  '.join(str(row) for row in self.matriz_adjacencia)
        string += '\n]'
        return string
    
    def add_edge(self, v1: str, v2: str, weight: float = 1, name: str = None):
        if(name in self.edges_map):
            raise ValueError("Edge name already exists")
        
        if(name is not None):
            name = str(name)

        v1 = str(v1)
        v2 = str(v2)
        
        if(v1 not in self.vertices_map):
            self.add_vertice(v1)
        
        if(v2 not in self.vertices_map):
            self.add_vertice(v2)
        
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        new_edge_paralel_index = len(self.matriz_adjacencia[v1_index][v2_index])
        
        self.matriz_adjacencia[v1_index][v2_index].append(Edge(name, weight))
        if name != None: self.edges_map[name] = (v1, v2, new_edge_paralel_index)
        
        if not self.DIRECTED and v1_index != v2_index:
            self.matriz_adjacencia[v2_index][v1_index].append(Edge(name, weight))
               
    def remove_edge_by_name(self, name: str):
        if name not in self.edges_map:
            raise ValueError("Edge name does not exist")
        
        v1, v2, parallel_index = self.edges_map[name]
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        
        self.matriz_adjacencia[v1_index][v2_index].pop(parallel_index)
        del self.edges_map[name]
        
        if not self.DIRECTED and v1_index != v2_index:
            self.matriz_adjacencia[v2_index][v1_index].pop(parallel_index)
        
        
    def remove_edge_by_vertices(self, v1: str, v2: str):
        v1 = str(v1)
        v2 = str(v2)
        
        if v1 not in self.vertices_map or v2 not in self.vertices_map:
            raise ValueError("Vertices does not exist")
        
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        
        for edge in self.matriz_adjacencia[v1_index][v2_index]:
            del self.edges_map[edge.name]
        
        self.matriz_adjacencia[v1_index][v2_index] = []
        if not self.DIRECTED:
            self.matriz_adjacencia[v2_index][v1_index] = []
               
    def add_vertice(self, name: str = None, weight: float = 0):
        if name in self.vertices_map:
            raise ValueError("Vertice already exists")
        
        new_vertice_index = len(self.matriz_adjacencia)
        new_size = new_vertice_index + 1
        
        if(name is None):
            name = str(new_size)
            
        self.vertices_map[name] = Node(new_vertice_index, weight)
        self.matriz_adjacencia.append([[] for _ in range(new_size)])
        
        for i in range(new_vertice_index):
            self.matriz_adjacencia[i].append([])
    
    def thers_vertice_adjacente(self, v1, v2):
        return self.matriz_adjacencia[v1][v2] != []
    
    def thers_edge_adjacence(self):
        pass
    
    def is_empty(self):
        return len(self.matriz_adjacencia) == 0
    
    
    
    def _create_matriz(self, rows, cols=None, value=[]):
        if cols is None:
            cols = rows
        return [[[] for _ in range(cols)] for _ in range(rows)]
    
    def _generate_vertice_name(self, index: int) -> str:
        resultado = ""
        while index >= 0:
            resultado = chr(index % 26 + ord('A')) + resultado
            index = index // 26 - 1
        return resultado

    def _fill_vertices_map(self, num_vertices, vertices):
        if not vertices:
            for i in range(num_vertices):
                self.vertices_map[i] = str(i+1)
        elif num_vertices == 0 or len(vertices) == num_vertices:
            self.matriz_adjacencia = self._create_matriz(len(vertices))
            for i in range(len(vertices)):
                vertice_name = str(vertices[i][0])
                vertice_weight = float(vertices[i][1])
                
                self.vertices_map[vertice_name] = Node(i, vertice_weight)
        else:
            raise ValueError("Number of vertices and vertices list does not match")