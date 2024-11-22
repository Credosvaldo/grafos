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
            self.edges_map: Dict[str, Tuple[str, str, int]] = {} # associando o nome da aresta com o nome dos nós na ponta e o indice da aresta (ou seja, qual coluna ela representa)
            self.DIRECTED = DIRECTED # Direcionado ou não
            
    def __str__(self) -> str:
        # Header with the names of the edges
        edge_names = [name for name in self.edges_map.keys()]
        edge_header = "    " + " ".join([f"{name:>5}" for name in edge_names]) + "\n"  # 5 characters per name, right-aligned

        # Body of the matrix with nodes and edge weights
        matrix_rows = []
        for node_name, node in self.nodes_map.items():
            node_index = node.index
            row_str = f"{node_name:<3} " + " ".join(  # Node name followed by weights of each edge
                [
                    f"{cell.weight:>5}" if cell else f"{'0':>5}"
                    for cell in self.matrix_incidency[node_index]
                ]
            )
            matrix_rows.append(row_str)

        # Subtitle for node weights
        subtitle_for_node_weights = "Legenda (Peso dos nós):\n" + "\n".join(
            [
                f"{node_name}: {node.weight}"
                for node_name, node in self.nodes_map.items()
            ]
        )

        # Building the final matrix
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
        i = 1
        new_edge_name = f"e{len(self.edges_map) + i}"
        while name is None or name in self.edges_map:
            name = str(new_edge_name)
            i += 1
            new_edge_name = f"e{len(self.edges_map) + 1}"
        
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
        # Remove a aresta da matriz de incidência (ou seja, apaga a coluna de cada linha) 
        for row in self.matrix_incidency:
            row.pop(edge_index)
        
        del self.edges_map[name]  # remove a aresta do mapeamento de arestas
        
        self._recreate_matrix()
        
    #Remove todas as arestas entre dois nós
    def remove_all_edges_by_nodes(self, predecessor: str, sucessor: str):
        v1 = str(predecessor)
        v2 = str(sucessor)
        
        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")
        
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        # Guarda todas as arestas que devem ser excluidas
        edges_to_remove = []
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # Verifica se há uma aresta entre v1 e v2 em qualquer direção
            if edge and (
                self.matrix_incidency[v2_index][edge_index] or  # (v1, v2)
                self.matrix_incidency[v1_index][edge_index]    # (v2, v1) - redundante, mas garante robustez
            ):
                edges_to_remove.append(edge_index)
        
        # Remove todas as arestas de tras pra frente para que o index das arestas não mude
        for edge_index in sorted(edges_to_remove, reverse=True):
            # Remove a coluna da matriz de incidência
            for row in self.matrix_incidency:
                row.pop(edge_index)
                
            # Encontra a chave no edges_map considerando ambas as direções
            edge_name = None
            for key, value in self.edges_map.items():
                if (value[0] == v1 and value[1] == v2 and value[2] == edge_index) or \
                (value[0] == v2 and value[1] == v1 and value[2] == edge_index):
                    edge_name = key
                    break
            
            if edge_name is not None:
                del self.edges_map[edge_name]
        
        self._recreate_matrix()

    def add_node(self, name: str, weight: float = 1):
        if name in self.nodes_map:
            raise ValueError(f"Já existe um nó com o nome {name}")
        
        new_node_index = len(self.nodes_map)
        self.nodes_map[name] = Node(index=new_node_index, weight=weight)
        
        # Verificando se há colunas suficientes na matriz para adicionar o novo nó
        num_columns = len(self.matrix_incidency[0]) if self.matrix_incidency else 0
        # Adicionando uma linha nova à matriz
        self.matrix_incidency.append([None for _ in range(num_columns)])
        
    def remove_node(self, name: str):
        name = str(name)
        
        if name not in self.nodes_map:
            raise ValueError("Node name does not exist")
        
        node_index = self.nodes_map[name].index
        
        # remove a linha da matrix
        self.matrix_incidency.pop(node_index)
        
        # remove todas as arestas que estavam conectadas ao ní
        edges_to_remove = []
        for edge_index, edge in enumerate(self.matrix_incidency[node_index] if self.matrix_incidency else []):
            if edge:
                edges_to_remove.append(edge_index)
        
        # Remove todas as arestas de trás pra frente para que o index das arestas não mude
        for edge_index in sorted(edges_to_remove, reverse=True):
            for row in self.matrix_incidency:
                row.pop(edge_index)
            
            # Agora buscamos as arestas no edges_map, considerando as duas direções
            # Ou seja, buscamos no edge_name um valor que tenha o edge_index e o nome do nó como origem ou destino
            edge_name = None
            for key, value in self.edges_map.items():
                if (value[0] == name and value[2] == edge_index) or (value[1] == name and value[2] == edge_index):
                    edge_name = key
                    break
            
            if edge_name is not None:
                del self.edges_map[edge_name]
        
        del self.nodes_map[name]
        
        self._recreate_matrix()
        
    def _recreate_matrix(self):
        # Atualiza os índices dos nós e das arestas após a remoção
        for i, (node_name, node) in enumerate(self.nodes_map.items()):
            node.index = i

        for j, edge_name in enumerate(self.edges_map.keys()):
            self.edges_map[edge_name] = (
                self.edges_map[edge_name][0], 
                self.edges_map[edge_name][1], 
                j
            )
        
    def thers_node_adjacente(self, predecessor: str, sucessor: str):
        v1 = str(predecessor)
        v2 = str(sucessor)
        
        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")
        
        # Index dos nós sendo avaliados
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        # Para cada coluna (ou seja, para cada aresta)
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # se existe uma aresta (ou seja, a matrix[linha][coluna] != None)
            if edge:
                # se o grafo for direcionado só é adjacente se sair de v1 e ir pra v2
                if self.DIRECTED:
                    if edge.weight < 0 and self.matrix_incidency[v2_index][edge_index]:
                        return True
                else:
                    # se for não direcionado, basta que a aresta ligue os dois nós
                    if self.matrix_incidency[v2_index][edge_index]:
                        return True
        return False
    
    