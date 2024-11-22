from typing import Dict, List, Tuple
from models.Edge import Edge
from models.Node import Node


class GrafoMI:
    
    def __init__(
        self,
        DIRECTED: bool = True,
        num_nodes: int = 0,
        nodes: List[Tuple[str, float]] = [],
        ):
            self.matrix_incidency: List[List[Edge]] = self._create_matrix(num_nodes) # eixo X são as arestas e o eixo Y são os vertices
            self.nodes_map: Dict[str, Node] = {} # associando o nome do nó com o nó 
            self.edges_map: Dict[str, Tuple[str, str, int]] # associando o nome da aresta com o nome dos nós na ponta e o indice da aresta (ou seja, qual coluna ela representa)
            self.DIRECTED = DIRECTED # Direcionado ou não
            self.excluded_nodes_index = [] # para não ter que apagar uma linha da matriz
            self.excluded_edges_intex = [] # para não ter que apagar uma coluna da matriz
            
            
    def __str__(self) -> str:
        # Header com o nome das arestas (ignorando as que foram excluídas)
        edge_names = [
            name for name, (_, _, index) in self.edges_map.items()
            if index not in self.excluded_edges_intex
        ]
        edge_header = "    " + " ".join([f"{name:>5}" for name in edge_names]) + "\n"  # 5 caracteres por nome e alinhado para a direita

        # Corpo da matriz com os nós e pesos das arestas (ignorando os que foram excluídos)
        matrix_rows = []
        for i, row in enumerate(self.matrix_incidency): # Iterar sobre cada linha da matriz -> i é o indice da linha e row é a linha
            if i in self.excluded_nodes_index:  # Ignorar nós excluídos
                continue
            
            node_name = list(self.nodes_map.keys())[i] 
            row_str = f"{node_name:<3} " + " ".join(  # Nome do nó seguido pelo peso de cada aresta
                [
                    f"{cell.weight:>5}" if cell and col_idx not in self.excluded_edges_intex else f"{'0':>5}"
                    for col_idx, cell in enumerate(row) # Iterar sobre cada célula da linha -> col_idx é o indice da coluna e cell é a célula
                    # celula é do tipo Edge
                ]
            )
            matrix_rows.append(row_str)
            
        
        subtitle_for_node_weights = "Legenda (Peso dos nós):\n".join(
            [
                f"{node_name}: {node_weight}"
                for node_name, node_weight in self.nodes_map.items()
            ]
        )
        # Construindo a matriz final
        result = "Matriz de Incidência:\n"
        result += edge_header
        result += "\n".join(matrix_rows)
        result += "\n\n" + subtitle_for_node_weights

        return result

    def _create_matrix(self, num_nodes: int, num_edges: int = 0):
        return [[None for _ in range(num_edges)] for _ in range(num_nodes)]
    
    # Recebemos quem a aresta liga, o nome e peso dela
    def add_edge(self, predecessor: str, sucessor: str, weight: float = 1, name: str = None):
        # Vemos o nome das arestas como únicos, então se já existir é erro
        if name != None and str(name) in self.edges_map:
            raise ValueError(f"Já existe uma aresta com o nome {name}")
        
        # se não tiver nome, criamos um
        new_edge_name = len(self.edges_map) + 1 
        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            new_edge_name += 1
        
        name = str(name)
        
        v1 = str(predecessor) # predecessor
        v2 = str(sucessor) # sucessor
        
        if v1 not in self.nodes_map:
            self.add_node(v1)
            
        if v2 not in self.nodes_map:
            self.add_node(v2)
            
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        # A aresta vai ser uma coluna nova na matriz
        # ela ligar v1 com v2, ou seja, se ela for não direcionada as linhas v1_index e v2_index vão ser as únicas com valor (igual ao peso)
        # se for direcionada a linha v1_index vai ser negativa (a aresta sai dela, igual ao peso) e a linha v2_index vai ser positiva
        # (a aresta chega nela, igual ao peso)
        
        # Adicionando a nova coluna à matriz
        new_edge_index = len(self.matrix_incidency[0])  # Novo índice da aresta (coluna da matriz)
        for row in self.matrix_incidency:
            row.append(None)  # Adiciona uma célula vazia para cada linha
        
        # Criando a nova aresta
        new_edge = Edge(name=name, weight=weight)
        self.matrix_incidency[v1_index][new_edge_index] = Edge(name=name, weight=-weight if self.DIRECTED else weight)
        self.matrix_incidency[v2_index][new_edge_index] = Edge(name=name, weight=weight)
        
        # Atualizando o mapeamento de arestas
        self.edges_map[name] = (v1, v2, new_edge_index)
        
    def remove_edge_by_name(self, name: str):
        name = str(name)
        
        # Só dá pra apagar se existe
        if name not in self.edges_map:
            raise ValueError("Edge name does not exist")
        
        _, _, edge_index = self.edges_map[name] # Pegando o índice da aresta
        self.excluded_edges_intex.append(edge_index) # Adicionando na lista de excluidos para não ter que refazer a matriz
        del self.edges_map[name] # apagando do mapeamento de arestas
        

    def add_node(self, name: str, weight: float = 1):
        if name in self.nodes_map:
            raise ValueError(f"Já existe um nó com o nome {name}")
        
        new_node_index = len(self.nodes_map)
        self.nodes_map[name] = Node(index=new_node_index, weight=weight)
        
        # Adicionando uma linha nova à matriz
        self.matrix_incidency.append([None for _ in range(len(self.matrix_incidency[0]))])