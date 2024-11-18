from typing import Dict, List, Tuple
from Edge import Edge
from Node import Node

class GrafoMA:
    
    def __init__(self, DIRECTED: bool = True, num_vertices: int = 0, vertices: List[Tuple[str, float]] = []):
        self.matriz_adjacencia = self._create_matriz(num_vertices)
        self.vertices_map: Dict[str, Node] = {}
        self.edges_map: Dict[str, Tuple[str, str, int]] = {}
        self.DIRECTED = DIRECTED
        self.excluded_vertices_index = []
        self._fill_vertices_map(num_vertices, vertices)
        
    def __str__(self) -> str:
        string = '[\n  '
        string += '\n  '.join(str(row) for i, row in enumerate(self.matriz_adjacencia) if i not in self.excluded_vertices_index)
        string += '\n]'
        return string
    
    def add_edge(self, v1: str, v2: str, weight: float = 1, name: str = None):
        if name != None and str(name) in self.edges_map:
            raise ValueError("Edge name already exists")
        
        new_edge_name = len(self.edges_map) + 1
        
        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            new_edge_name += 1
            
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
        self.edges_map[name] = (v1, v2, new_edge_paralel_index)
        
        if not self.DIRECTED and v1_index != v2_index:
            self.matriz_adjacencia[v2_index][v1_index].append(Edge(name, weight))
               
    def remove_edge_by_name(self, name: str):
        name = str(name)
        
        if name not in self.edges_map:
            raise ValueError("Edge name does not exist")
        
        v1, v2, parallel_index = self.edges_map[name]
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        
        self.matriz_adjacencia[v1_index][v2_index].pop(parallel_index)
        del self.edges_map[name]
        
        if not self.DIRECTED and v1_index != v2_index:
            self.matriz_adjacencia[v2_index][v1_index].pop(parallel_index)
        
    # Remove all edges between two vertices
    def remove_all_edge_by_vertices(self, v1: str, v2: str):
        v1 = str(v1)
        v2 = str(v2)
        
        if v1 not in self.vertices_map or v2 not in self.vertices_map:
            raise ValueError("Vertices does not exist")
        
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        
        
        for edge in self.matriz_adjacencia[v1_index][v2_index]:
            self.edges_map.pop(edge.name)
        self.matriz_adjacencia[v1_index][v2_index] = []
        
        if not self.DIRECTED:
            for edge in self.matriz_adjacencia[v2_index][v1_index]:
                self.edges_map.pop(edge.name)
            self.matriz_adjacencia[v2_index][v1_index] = []
               
    def add_vertice(self, name: str = None, weight: float = 0):
        if str(name) in self.vertices_map:
            raise ValueError("Vertice already exists")      
        
        matriz_size = len(self.matriz_adjacencia)
        vertice_name_index = matriz_size
        new_size = matriz_size + 1

        if self.excluded_vertices_index:
            new_vertice_index = self.excluded_vertices_index.pop(0)
            usin_a_excluded_vertice = True
        else:
            new_vertice_index = len(self.matriz_adjacencia)
            usin_a_excluded_vertice = False
            
        while name is None or name in self.vertices_map:
            name = str(vertice_name_index)
            vertice_name_index += 1
            
        name = str(name)
        self.vertices_map[name] = Node(new_vertice_index, weight)
        
        if usin_a_excluded_vertice:
            return
        
        self.matriz_adjacencia.append([[] for _ in range(new_size)])
        for i in range(matriz_size):
            self.matriz_adjacencia[i].append([])
    
    def remove_vertice(self, name: str):
        name = str(name)
        
        if name not in self.vertices_map:
            raise ValueError("Vertice does not exist")
        
        vertice_index = self.vertices_map[name].index
        self.excluded_vertices_index.append(vertice_index)
        
        for i in range(len(self.matriz_adjacencia)):
            for edge in self.matriz_adjacencia[i][vertice_index]:
                del self.edges_map[edge.name]
                    
            if self.DIRECTED:
                for edge in self.matriz_adjacencia[vertice_index][i]:
                    del self.edges_map[edge.name]
                    
            self.matriz_adjacencia[i][vertice_index] = []
            self.matriz_adjacencia[vertice_index][i] = []
        
        self.vertices_map.pop(name)
    
    def thers_vertice_adjacente(self, v1: str, v2: str):        
        v1 = str(v1)
        v2 = str(v2)
        
        if v1 not in self.vertices_map or v2 not in self.vertices_map:
            raise ValueError("Vertices does not exist")
        
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        
        return self.matriz_adjacencia[v1_index][v2_index] != []
    
    def thers_edge_adjacence(self, ed1: str, ed2: str):
        ed1 = str(ed1)
        ed2 = str(ed2)
        
        vertices_ed1 = self.edges_map[ed1]
        vertices_ed2 = self.edges_map[ed2]
        
        return any(v in vertices_ed2[:2] for v in vertices_ed1[:2])
        
    def thers_edge_by_name(self, name: str):
        name = str(name)
        return name in self.edges_map
    
    def thers_edge_by_vertices(self, v1: str, v2: str):
        v1 = str(v1)
        v2 = str(v2)
    
        v1_index = self.vertices_map[v1].index
        v2_index = self.vertices_map[v2].index
        
        return self.matriz_adjacencia[v1_index][v2_index] != []
        
    def get_edge_count(self):
        return len(self.edges_map)
    
    def get_vertice_count(self):
        return len(self.vertices_map)
    
    def is_empty(self):
        return len(self.matriz_adjacencia) - len(self.excluded_vertices_index) == 0
    
    def is_complete(self):
        size = len(self.matriz_adjacencia)
        for i in range(size):
            for j in range(size):
                if i != j and len(self.matriz_adjacencia[i][j]) != 1:
                    return False
                if i == j and len(self.matriz_adjacencia[i][j]) != 0:
                    return False
        return True
    
    
    def _create_matriz(self, rows, cols=None):
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