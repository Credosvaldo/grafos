from typing import Dict, List, Union
import Grafo
from Edge import Edge
from Node import Node

from functools import singledispatchmethod

class GrafoMA:
    
    def __init__(self, DIRECTED: bool, num_vertices: int = 0):
        self.matriz_adjacencia = self._create_matriz(num_vertices)
        self.vertices_map: Dict[str, Node] = {}
        self.DIRECTED = DIRECTED
        
        for i in range(num_vertices):
            vertice_name = self._generate_vertice_name(i)
            self.vertices_map[vertice_name] = Node(i)
            
        
    def __str__(self) -> str:
        string = '[\n  '
        string += '\n  '.join(str(row) for row in self.matriz_adjacencia)
        string += '\n]'
        return string
    
    @singledispatchmethod
    def add_edge(self, v1, v2, w):
        raise NotImplementedError("Unsupported type")

    @add_edge.register
    def _(self, v1: int, v2: int, w: float = 1):
        self.matriz_adjacencia[v1][v2].append(Edge(weight=w))
        
        if not self.DIRECTED:
            self.matriz_adjacencia[v2][v1].append(Edge(weight=w))
            
    @add_edge.register
    def _(self, v1: str, v2: str, w: float = 1):
        if(v1 not in self.vertices_map):
            add_vertice(v1)
        
        if(v2 not in self.vertices_map):
            add_vertice(v2)
        
        str_v1 = self.vertices_map[v1].index
        str_v2 = self.vertices_map[v2].index
        
        self.matriz_adjacencia[str_v1][str_v2].append(Edge(weight=w))
        
        if not self.DIRECTED:
            self.matriz_adjacencia[v2][v1] = w
            
              
    def add_vertice(self, name=None, weight=0):
        new_vertice_index = len(self.matriz_adjacencia)
        vertice_index_name = new_vertice_index
        new_size = new_vertice_index + 1
        
        if name in self.vertices_map:
            raise ValueError("Vertice already exists")
        
        while name in self.vertices_map or name is None:
            name = self._generate_vertice_name(vertice_index_name)
            vertice_index_name+=1
            
        self.vertices_map[name] = Node(new_vertice_index, weight)
            
        self.matriz_adjacencia.append([[]] * new_size)
        for i in range(new_vertice_index):
            self.matriz_adjacencia[i].append([])
    
    def thers_vertice_adjacente(self, v1, v2):
        return self.matriz_adjacencia[v1][v2] is not None
    
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
