from typing import Dict, List, Tuple
from IGrafo import IGrafo
from enums.ConnectivityDegree import ConnectivityDegree
from models.TarjansNode import TarjansNode
from models.DFSNode import DFSNode
from models.Edge import Edge
from models.Node import Node
import xmltodict
from multiprocessing import Process
import copy


class GrafoMI(IGrafo):

    def __init__(
        self,
        DIRECTED: bool = True,
        num_nodes: int = 0,
        nodes: List[Tuple[str, float]] = [],
    ):
        self.matrix_incidency: List[List[Edge]] = self._create_matrix(
            num_nodes
        )  # eixo X são as arestas e o eixo Y são os vertices
        self.nodes_map: Dict[str, Node] = {}  # associando o nome do nó com o nó
        self.edges_map: Dict[str, Tuple[str, str, int, float]] = (
            {}
        )  # associando o nome da aresta com o nome dos nós na ponta e o indice da aresta (ou seja, qual coluna ela representa)
        self.DIRECTED = DIRECTED  # Direcionado ou não
        self._fill_nodes_map(num_nodes, nodes)

    def __str__(self) -> str:
        # Header with the names of the edges
        edge_names = [name for name in self.edges_map.keys()]
        edge_header = (
            "    " + " ".join([f"{name:>5}" for name in edge_names]) + "\n"
        )  # 5 characters per name, right-aligned

        # Body of the matrix with nodes and edge weights
        matrix_rows = []
        for node_name, node in self.nodes_map.items():
            node_index = node.index
            row_str = (
                f"{node_name:<3} "
                + " ".join(  # Node name followed by weights of each edge
                    [
                        f"{cell.weight:>5}" if cell else f"{'0':>5}"
                        for cell in self.matrix_incidency[node_index]
                    ]
                )
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
    def add_edge(
        self, predecessor: str, successor: str, weight: float = 1, name: str = None
    ):
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

        v1 = str(predecessor)  # predecessor
        v2 = str(successor)  # successor

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
        new_edge_index = len(
            self.matrix_incidency[0]
        )  # Novo índice da aresta (coluna da matriz)
        for row in self.matrix_incidency:
            row.append(None)  # Adiciona uma célula vazia para cada linha

        # Criando a nova aresta
        new_edge = Edge(name=name, weight=weight)
        if v1_index != v2_index:
            self.matrix_incidency[v1_index][new_edge_index] = Edge(
                name=name, weight=-1 if self.DIRECTED else 1
            )
            self.matrix_incidency[v2_index][new_edge_index] = Edge(name=name, weight=1)
        else:
            self.matrix_incidency[v1_index][new_edge_index] = Edge(name=name, weight=2)

        # Atualizando o mapeamento de arestas
        self.edges_map[name] = (v1, v2, new_edge_index, weight)
        return name

    def remove_edge_by_name(self, name: str):
        name = str(name)

        # Só dá pra apagar se existe
        if name not in self.edges_map:
            raise ValueError("Edge name does not exist")

        _, _, edge_index, _ = self.edges_map[name]  # Pegando o índice da aresta
        # Remove a aresta da matriz de incidência (ou seja, apaga a coluna de cada linha)
        for row in self.matrix_incidency:
            row.pop(edge_index)

        del self.edges_map[name]  # remove a aresta do mapeamento de arestas

        self._recreate_matrix()

    # Remove todas as arestas entre dois nós
    def remove_all_edges_by_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        # Guarda todas as arestas que devem ser excluidas
        edges_to_remove = []
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # Verifica se há uma aresta entre v1 e v2 em qualquer direção
            if edge and (
                self.matrix_incidency[v2_index][edge_index]  # (v1, v2)
                or self.matrix_incidency[v1_index][
                    edge_index
                ]  # (v2, v1) - redundante, mas garante robustez
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
                if (value[0] == v1 and value[1] == v2 and value[2] == edge_index) or (
                    value[0] == v2 and value[1] == v1 and value[2] == edge_index
                ):
                    edge_name = key
                    break

            if edge_name is not None:
                del self.edges_map[edge_name]

        self._recreate_matrix()

    def add_node(self, name: str, weight: float = 1.0):
        name = str(name)
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
        for edge_index, edge in enumerate(
            self.matrix_incidency[node_index] if self.matrix_incidency else []
        ):
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
                if (value[0] == name and value[2] == edge_index) or (
                    value[1] == name and value[2] == edge_index
                ):
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
                j,
                self.edges_map[edge_name][3],
            )

    def thers_node_adjacency(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")

        # Index dos nós sendo avaliados
        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        # Para cada coluna (ou seja, para cada aresta)
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # se existe uma aresta (ou seja, a matrix[linha][coluna] != None)
            if edge:
                if predecessor == successor:
                    if edge.weight == 2:
                        return True
                    else:
                        return False
                    
                # se o grafo for direcionado só é adjacente se sair de v1 e ir pra v2
                if self.DIRECTED:
                    if edge.weight < 0 and self.matrix_incidency[v2_index][edge_index]:
                        return True
                else:
                    # se for não direcionado, basta que a aresta ligue os dois nós
                    if self.matrix_incidency[v2_index][edge_index]:
                        return True
        return False

    def thers_only_one_edge_btwn_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        # Para cada coluna (ou seja, para cada aresta)
        count = 0
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # se existe uma aresta (ou seja, a matrix[linha][coluna] != None)
            if edge:
                # se o grafo for direcionado só é adjacente se sair de v1 e ir pra v2
                if self.DIRECTED:
                    if edge.weight < 0 and self.matrix_incidency[v2_index][edge_index]:
                        count += 1
                else:
                    # se for não direcionado, basta que a aresta ligue os dois nós
                    if self.matrix_incidency[v2_index][edge_index]:
                        count += 1
        return count == 1

    def thers_edge_adjacency(self, edge1: str, edge2: str):
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

    def thers_edge_by_nodes(self, predecessor: str, successor: str):
        v1 = str(predecessor)
        v2 = str(successor)

        if v1 not in self.nodes_map or v2 not in self.nodes_map:
            raise ValueError("Node does not exist")

        v1_index = self.nodes_map[v1].index
        v2_index = self.nodes_map[v2].index

        # Para cada coluna (ou seja, para cada aresta)
        for edge_index, edge in enumerate(self.matrix_incidency[v1_index]):
            # se a aresta existir na linha do v1 (ou seja, a matrix[linha][coluna] != None)
            if edge:
                # se o grafo for direcionado a aresta tem que sair do predecessor e ir pro successor
                # ou seja, o peso tem que ser negativo e a coluna tem que existir no successor
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
        for v1_name in self.nodes_map.keys():
            for v2_name in self.nodes_map.keys():
                if v1_name != v2_name and not self.thers_only_one_edge_btwn_nodes(
                    v1_name, v2_name
                ):
                    return False
                if v1_name == v2_name and self.thers_node_adjacency(v1_name, v2_name):
                    return False
        return True

    def is_simple(self):
        # Verificar se há laços
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index, _ = edge_info
            if v1 == v2:
                return False

        # Verificar se há arestas paralelas
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index, _ = edge_info
            for other_edge_name, other_edge_info in self.edges_map.items():
                if edge_name != other_edge_name:
                    other_v1, other_v2, _, _ = other_edge_info
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

        # adiciona as arestas trocando successor por predecessor
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index, _ = edge_info
            if v1 != v2:
                # troca o sinal do peso da aresta pq como é direcionado o peso da aresta saindo de v1 tá negativo
                edge_weight = (
                    self.matrix_incidency[self.nodes_map[v1].index][edge_index].weight * -1
                )
                new_graph.add_edge(v2, v1, edge_weight, edge_name)
            else:
                new_graph.add_edge(v1, v2, 2, edge_name)

        return new_graph

    def make_underlying_graph(self):
        # faz o grafo subjacente, ou seja, transforma um grafo direcionado em não dir
        # Se já for não direcionado lança erro
        if not self.DIRECTED:
            raise ValueError("Cannot make underlying graph of a non-directed graph")

        # cria um novo grafo
        new_graph = GrafoMI(DIRECTED=False)

        # adiciona os mesmos vertices a esse grafo
        for name, node in self.nodes_map.items():
            new_graph.add_node(name, node.weight)

        # adiciona as arestas ao grafo subjacente
        for edge_name, edge_info in self.edges_map.items():
            v1, v2, edge_index, _ = edge_info
            if v1 != v2:
                # troca o sinal do peso da aresta pq como é direcionado o peso da aresta saindo de v1 tá negativo
                edge_weight = (
                    self.matrix_incidency[self.nodes_map[v1].index][edge_index].weight * -1
                )
                new_graph.add_edge(v2, v1, edge_weight, edge_name)
            else:
                new_graph.add_edge(v2, v1, edge_weight, edge_name)

        return new_graph

    def _non_directed_connectivity_degree(self):
        # Inicializa um conjunto para nós visitados
        visited = set()

        # Busca em profundidade a partir de um nó inicial para ver se dá pra alcançar td mundo
        def dfs_for_connectivity(node_index):
            visited.add(node_index)  # adiciona o nó atual nos visitados
            for edge_index, edge in enumerate(self.matrix_incidency[node_index]):
                if edge:  # se tiver uma aresta conectada no nó sendo analisado
                    # ver quem que a aresta conecta
                    # se for loop a gnt pula pra proxima iteração
                    v1 = self.edges_map[edge.name][0]
                    v2 = self.edges_map[edge.name][1]

                    v1_index = self.nodes_map[v1].index
                    v2_index = self.nodes_map[v2].index

                    # se a aresta liga v1 com v2
                    if v1_index == node_index and v2_index != node_index:
                        # e v1 == nó sendo avaliado, o vizinho é v2
                        neighbor = v2
                    elif v2_index == node_index and v1_index != node_index:
                        # se v2 == nó sendo avaliado, o vizinho é v1
                        neighbor = v1
                    else:
                        # se for loop siginifica que já adicionamos aos nós visitados quando começou essa iteração
                        # então podemos passar para a proxima aresta conectada a esse nó
                        continue

                    neighbor_index = self.nodes_map[neighbor].index
                    if neighbor_index not in visited:
                        # se ele ainda não foi visitado fazemos uma busca em profundidade nele
                        dfs_for_connectivity(neighbor_index)

        # Começa a DFS do primeiro nó disponível
        start_node_index = next(iter(self.nodes_map.values())).index
        dfs_for_connectivity(start_node_index)

        # Verifica se todos os nós foram visitados
        return len(visited) == len(self.nodes_map)

    def connectivity_degree(self):
        # Verifica se o grafo não é direcionado
        if not self.DIRECTED:
            # Se for não direcionado, basta verificar a conectividade
            if self._non_directed_connectivity_degree():
                return ConnectivityDegree.STRONGLY_CONNECTED
            else:
                return ConnectivityDegree.DISCONNECTED
        else:
            # Grafo direcionado: verificamos primeiro a semi-forte conectividade.
            underlying_graph = self.make_underlying_graph()
            if not underlying_graph._non_directed_connectivity_degree():
                return ConnectivityDegree.DISCONNECTED

            semifortemente = False
            # Verifica se é fortemente conexo
            for node in self.nodes_map:
                reachable = self._get_reachable_nodes(node)
                if len(reachable) != len(self.nodes_map):
                    # Se o nó não alcança todos os outros temos que ver se os que faltam alcança o nó
                    # para isso primeiro pegamos um set com os nós que faltam
                    missing_nodes = set(self.nodes_map.keys()) - reachable
                    # depois montamos um grafo reverso
                    revert_graph = self.make_revert_graph()
                    # depois iteramos sobre os nós que faltam e vemos se eles alcançam o nó
                    for missing_node in missing_nodes:
                        nodes_that_reach_the_current_node = (
                            revert_graph._get_reachable_nodes(node)
                        )
                        if missing_node not in nodes_that_reach_the_current_node:
                            # Como já provamos que o grafo é conexo
                            # Se algum nó não alcança e nem é alcançado por outro
                            # o grafo é simplesmente conexo
                            return ConnectivityDegree.WEAKLY_CONNECTED
                    # se passamos da verificação de simplesmente conexo
                    # significa que o nó atual (node) não alcança algum nó, mas esse nó alcança ele
                    # então o grafo é no máximo semi-fortemente conexo
                    # não dou um early return aqui pq pode ser que algum nó futuro não alcance nem seja alcançado por algum nó
                    semifortemente = True

            if semifortemente:
                return (
                    ConnectivityDegree.UNIDIRECTIONAL_CONNECTED
                )  # se todos os nós são alcançados por todos é semi-fortemente conexo
            return (
                ConnectivityDegree.STRONGLY_CONNECTED
            )  # se todos alcançam todos é fortemente conexo

    def _depth_first_search(self):
        # inicializa o tempo zerado
        time = [0]
        # inicializa a tabela do resultado com a key sendo o nome do nó e o valor o TD, TT e pai
        result = self._get_dfs_result_structure()

        # para cada nó que não foi visitado, fazemos uma busca em profundidade
        numbers_of_trees = 0  # numero de arvores (para o kosaraju)
        for node_name, node_value in result.items():
            if node_value.discovery_time == 0:
                self._dfs(node_name, time, result)

        return result

    def _dfs(self, node_name: str, time: list[int], result: Dict[str, DFSNode]):
        node_name = str(node_name)
        # Soma um ao contador global
        time[0] += 1
        # Atribui o tempo de descoberta do nó
        result[node_name].discovery_time = time[0]

        # Para cada coluna da matriz
        for edge_index, edge in enumerate(
            self.matrix_incidency[self.nodes_map[node_name].index]
        ):
            # se há uma aresta saindo do nó em analise
            if edge:
                # Pega o nome do nó que a aresta liga
                other_node_name = self.edges_map[edge.name][1]
                # Se o nó não foi descoberto, fazemos uma busca em profundidade nele
                if result[other_node_name].discovery_time == 0:
                    result[other_node_name].parent = node_name
                    self._dfs(other_node_name, time, result)

        # Chegando no final da busca em profundidade, incrementamos o contador global e atribuimos o TT
        time[0] += 1
        result[node_name].finishing_time = time[0]

    def _get_reachable_nodes(self, start_node_name):
        # Busca em profundidade para pegar todos os nós alcançáveis a partir de um nó inicial
        visited = set()  # nós alcançados
        stack = [start_node_name]  # Começa o stack com o nó inicial
        while stack:  # enquanto stack não estiver vazio
            current = (
                stack.pop()
            )  # considera o nó atual como o último a ser adicionado ao stack
            if current not in visited:  # se o nó não foi visitado ainda
                visited.add(current)  # adiciona ele aos visitados
                current_index = self.nodes_map[
                    current
                ].index  # pega o index do nó atual
                for edge_index, edge in enumerate(
                    self.matrix_incidency[current_index]
                ):  # para cada coluna na linha do nó atual
                    if (
                        edge and edge.weight < 0
                    ):  # se tiver uma aresta saindo do nó atual
                        neighbor = self.edges_map[edge.name][
                            1
                        ]  # pega o destino da aresta
                        if neighbor not in visited:  # ve se ele já foi visitado
                            stack.append(neighbor)  # adiciona ao stakck
        return visited

    # region XML Section
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

            self.add_edge(source, target, float(edge["@weight"]), edge["@label"])
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

        with open("output/graphMI.gexf", "w") as file:
            file.write(result)

    def __writeGraph(self):
        result = '<attributes class="node">\n'
        result += '<attribute id="0" title="weight" type="float"/>\n'
        result += "</attributes>\n"
        result += "<nodes>\n"
        for node in self.nodes_map.keys():
            result += self.__writeNode(node)
        result += "</nodes>\n"
        result += "<edges>\n"
        for name in self.edges_map:

            result += self.__writeEdge(name)
        result += "</edges>\n"
        return result

    def __writeNode(self, node_name: str):
        node = self.nodes_map[node_name]
        result = f'<node id="{node_name}" label="{node_name}">\n'
        result += "<attvalues>\n"
        result += '<attvalue for="0" value="' + str(node.weight) + '"/>\n'
        result += "</attvalues>\n"
        result += "</node>\n"

        return result

    def __writeEdge(self, edge: str):

        predecessor, successor, _, weight = self.edges_map[edge]

        result = f"<edge label='{edge}' source='{predecessor}' target='{successor}' weight='{weight}'/>\n"

        return result

    # endregion

    def kosaraju(self):
        # Algoritmo de Kosaraju para encontrar componentes fortemente conexos
        # Primeiro fazemos uma busca em profundidade no grafo subjacente
        dfs_result = self._depth_first_search()
        # ao mesmo tempo pegamos o grafo reverso do grafo original
        grafo_reverso = self.make_revert_graph()
        # Depois fazemos uma busca em profundidade no grafo reverso em ordem decrescente de TT
        # pegar os nós em ordem decrescente de TT
        sorted_nodes = sorted(
            dfs_result.items(), key=lambda item: item[1].finishing_time, reverse=True
        )
        sorted_node_names = [node_name for node_name, _ in sorted_nodes]

        visited = set()  # nós visitados
        strongly_connected_components = (
            []
        )  # componentes (conjuntos de vértices) fortemente conexos

        for node_name in sorted_node_names:
            if node_name not in visited:
                # Executar busca em profundidade para encontrar todos os nós alcançáveis
                reachable_nodes = grafo_reverso._get_reachable_nodes(node_name)
                strongly_connected_components.append(reachable_nodes)
                visited.update(reachable_nodes)

        return len(strongly_connected_components)

    def get_articulations(self):  # metodo "naive" de verificar se é articulação
        if self.is_empty():  # se o grafo for vazio não tem como ter articulações
            return []

        articulations = []  # lista de articulações
        graph_copy = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )  # copia do grafo para não alterar o original

        # verifica se o grafo já não é deconexo (não tem articulações)
        if not graph_copy._non_directed_connectivity_degree():
            return articulations

        for node_name in self.nodes_map.keys():  # para cada nó do grafo
            # salva as arestas que vão ser removidas ao remover o nó
            edges_names_to_remove = [
                edge_name
                for edge_name, edge_info in graph_copy.edges_map.items()
                if node_name in edge_info[:2]
            ]
            edges_to_remove = []
            for edge_name in edges_names_to_remove:
                v1, v2, _, weight = graph_copy.edges_map[edge_name]
                edges_to_remove.append((v1, v2, weight, edge_name))

            graph_copy.remove_node(node_name)  # remove o nó
            if (
                not graph_copy._non_directed_connectivity_degree()
            ):  # se o grafo deixou de ser conexo
                articulations.append(node_name)  # era articulação
            graph_copy.add_node(node_name)  # retorna o nó para o grafo copia

            # retorna as arestas removidas
            for v1, v2, weight, edge_name in edges_to_remove:
                graph_copy.add_edge(v1, v2, weight, edge_name)
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

    def is_connected(self):
        return self._non_directed_connectivity_degree()

    def get_bridge(self):
        if self.is_empty():
            return []  # se o grafo for vazio não tem como ter pontes

        bridges = []  # lista de pontes
        graph_copy = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )

        # verifica se o grafo já não é deconexo (não tem pontes)
        if not graph_copy._non_directed_connectivity_degree():
            return bridges

        # Faz uma cópia das chaves das arestas para evitar modificar durante a iteração
        edges = list(graph_copy.edges_map.items())

        # Para cada aresta do grafo
        for edge_name, edge_info in edges:
            v1, v2, index, weight = edge_info  # Pega as informações da aresta
            graph_copy.remove_edge_by_name(edge_name)  # Remove a aresta
            if (
                not graph_copy._non_directed_connectivity_degree()
            ):  # Se o grafo deixou de ser conexo
                bridges.append(edge_name)  # É ponte
            graph_copy.add_edge(
                v1, v2, weight, edge_name
            )  # Retorna a aresta ao grafo copia

        return bridges

    def get_all_nodes_degree(self):
        nodes_degree: Dict[str, int] = {}
        for node_name in self.nodes_map.keys():
            nodes_degree[node_name] = 0
            for edge_name, edge_info in self.edges_map.items():
                if node_name in edge_info[:2]:
                    nodes_degree[node_name] += 1
        return nodes_degree

    def get_edges_by_node(self, node_name: str):
        edges = []
        for edge_name, edge_info in self.edges_map.items():
            if node_name in edge_info[:2]:
                edges.append(edge_name)
        return edges

    def is_bridge(self, edge_name: str):
        """
        Check if the given edge is a bridge.
        Args:
            edge_name (str): The edge name.
        Returns:
            bool: True if the edge is a bridge, False otherwise.
        """
        if edge_name not in self.edges_map:
            raise ValueError("Edge name does not exist")

        copy_graph = (
            self.make_underlying_graph() if self.DIRECTED else copy.deepcopy(self)
        )

        v1, v2, _, _ = copy_graph.edges_map[edge_name]
        copy_graph.remove_edge_by_name(edge_name)

        is_bridge = not copy_graph.reachable(v1, v2)

        return is_bridge

    def get_euler_path(self, by_tarjan: bool = True):
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

            is_bridge = False
            if len(edges_of_current_node) == 1:
                chosen_edge = edges_of_current_node[0]
                is_bridge = True
            else:
                for edge in edges_of_current_node:
                    if not is_bridge_method(edge):
                        chosen_edge = edge
                        break

            v1, v2, _, _ = copy_graph.edges_map[chosen_edge]
            if is_bridge:
                copy_graph.remove_node(current_node)
            else:
                copy_graph.remove_edge_by_name(chosen_edge)
            current_node = v2 if v1 == current_node else v1

        if copy_graph.get_edge_count() != 0:
            raise ValueError("Graph has more than one connected component")

        euler_path.append(current_node)
        return euler_path

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

        for v in self.matrix_incidency[node_index]:
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

        for v in self.get_edges_by_node(node_name):
            v1, v2, _, _ = self.edges_map[v]
            neibor = v2 if v1 == node_name else v1

            if not result[neibor].visited:
                result[neibor].parent = node_name

                self._tarjan_dfs(neibor, result, bridges, time)

                result[node_name].low = min(result[node_name].low, result[neibor].low)

                if result[neibor].low > result[node_name].disc:
                    bridges.append(v)

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

    def is_bridge_by_tarjan(self, edge_name: str):
        if self.is_empty():
            return []

        time = [0]
        bridges: List[str] = []

        result: Dict[str, TarjansNode] = {}

        for node_name in self.nodes_map.keys():
            result[node_name] = TarjansNode(False, None, 0, 0)

        v1, _, _, _ = self.edges_map[edge_name]

        self._tarjan_dfs(v1, result, bridges, time)

        return edge_name in bridges

    def reachable(self, v1: str, v2: str, results: Dict[str, Dict[str, DFSNode]] = {}):
        v1 = str(v1)
        v2 = str(v2)

        if v1 not in results.keys():
            result = self._get_dfs_result_structure()
            self._dfs(v1, [0], result)
            results[v1] = result

        return results[v1][v2].discovery_time != 0

    def _get_dfs_result_structure(self, nodes_group: List[str] = None):
        if nodes_group == None:
            nodes_group = self.nodes_map.keys()

        result: Dict[str, DFSNode] = {}
        for node_name in nodes_group:
            result[node_name] = DFSNode(0, 0, None)
        return result
