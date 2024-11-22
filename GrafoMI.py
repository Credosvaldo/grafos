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
            self._fill_nodes_map(num_nodes, nodes)
            
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
        
        
        # remove a linha da matrix
        self.matrix_incidency.pop(node_index)
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
    
    def theres_edge_adjacente(self, edge1: str, edge2: str):
        if edge1 not in self.edges_map or edge2 not in self.edges_map:
            raise ValueError("Edge does not exist")
        
        v1, v2, edge1_index = self.edges_map[edge1]
        v3, v4, edge2_index = self.edges_map[edge2]
        
        # A aresta vai ser adjancete se ela tiver um nó em comum
        # no caso do grafo direcionado, o nó comum tem que ser no destino/origem
        if self.DIRECTED:
            return v2 == v3
        else:
            # no grafo não direcionado se qualquer um dos vertices for igual é adj
            return v2 == v3 or v2 == v4 or v1 == v3 or v1 == v4
    
    def thers_edge_by_name(self, name: str):
        return str(name) in self.edges_map
    
    def thers_edge_by_nodes(self, predecessor: str, sucessor: str):
        v1 = str(predecessor)
        v2 = str(sucessor)
        
        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")
        
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index
        
        # Para cada coluna (ou seja, para cada aresta)
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # se a aresta existir na linha do v1 (ou seja, a matrix[linha][coluna] != None)
            if edge:
                # se o grafo for direcionado a aresta tem que sair do predecessor e ir pro sucessor
                # ou seja, o peso tem que ser negativo e a coluna tem que existir no sucessor
                if self.DIRECTED:
                    if edge.weight < 0 and self.matrix_incidency[v2_index][edge_index]:
                        return True
                else:
                    # se for não direcionado, basta que a aresta ligue os dois nós
                    if self.matrix_incidency[v2_index][edge_index]:
                        return True
        return False
    
    def get_edge_count(self):
        return len(self.edges_map)
    
    def get_node_count(self):
        return len(self.nodes_map)
    
    def is_empty(self):
        return len(self.nodes_map) == 0
    
    def is_complete(self):
        # um grafo é completo se todos os nós forem diretamente adjacentes a todos os outros nós
        for node1_name, node1 in self.nodes_map.items():
            for node2_name, node2 in self.nodes_map.items():
                if node1_name != node2_name and not self.thers_node_adjacente(node1_name, node2_name):
                    return False
        return True
    
    def is_simple(self):
        # Verificar se há laços
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index = edge_info
            if v1 == v2:
                return False
        
        # Verificar se há arestas paralelas
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index = edge_info
            for other_edge_name, other_edge_info in self.edges_map.items():
                if edge_name != other_edge_name:
                    other_v1, other_v2, _ = other_edge_info
                    if self.DIRECTED:
                        # Verificar se as arestas têm os mesmos dois vértices, na mesma direção
                        if v1 == other_v1 and v2 == other_v2:
                            return False
                    else:
                        # Verificar se as arestas têm os mesmos dois vértices, independentemente da direção
                        if {v1, v2} == {other_v1, other_v2}: 
                            return False
        
        # Se não encontrar laços ou arestas paralelas, o grafo é simples
        return True
    
    def _generate_node_name(self, index: int) -> str:
        resultado = ""
        while index >= 0:
            resultado = chr(index % 26 + ord("A")) + resultado
            index = index // 26 - 1
        return resultado

    def _fill_nodes_map(self, num_nodes: int, nodes: Node):
        if not nodes:
            for i in range(num_nodes):
                self.add_node(self._generate_node_name(i))
        elif num_nodes == 0 or len(nodes) == num_nodes:
            for node in nodes:
                self.add_node(node.index, node.weight)
        else:
            raise ValueError("Number of nodes and nodes list does not match")
        
    def make_revert_graph(self):
        # cria um gafo com as arestas no sentido contrario as arestas do grafo origial
        # se o grafo não for direcionado joga value error
        if not self.DIRECTED:
            raise ValueError("Cannot revert a non-directed graph")
        
        # cria um novo grafo
        new_graph = GrafoMI(DIRECTED=self.DIRECTED)
        
        # adiciona os mesmos vertices a esse grafo
        for name, node in self.nodes_map.items():
            new_graph.add_node(name, node.weight)
            
        # adiciona as arestas trocando sucessor por predecessor
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index = edge_info
            # troca o sinal do peso da aresta pq como é direcionado o peso da aresta saindo de v1 tá negativo
            edge_weight = self.matrix_incidency[self.nodes_map[v1].index][edge_index].weight * -1
            new_graph.add_edge(v2, v1, edge_weight, edge_name)
        
        return new_graph