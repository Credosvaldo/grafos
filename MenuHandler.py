from IGrafo import IGrafo

def options_switch(opcao: int, graph: IGrafo):
    # adicionar nó
    if opcao == 1:
        _add_node(graph)
    # remover nó
    elif opcao == 2:
        _remove_node(graph)
    # adicionar aresta
    elif opcao == 3:
        _add_edge(graph)
    # remover aresta pelo nome
    elif opcao == 4:
        _remove_edge_by_name(graph)
    # remover todas as arestas entre dois nós
    elif opcao == 5:
        _remove_all_edges_by_nodes(graph)
    # verificar adjacência entre dois nós
    elif opcao == 6:
        _thers_node_adjacency(graph)
    # verificar adjacência entre duas arestas
    elif opcao == 8:
        _thers_edge_adjacency(graph)
    # verificar se há aresta pelo nome
    elif opcao == 9:
        _thers_edge_by_name(graph)
    # verificar se há aresta entre dois nós
    elif opcao == 10:
        _thers_edge_by_nodes(graph)
    # contar arestas
    elif opcao == 11:
        _get_edge_count(graph)
    # contar nós
    elif opcao == 12:
        _get_node_count(graph)
    # verificar se o grafo está vazio
    elif opcao == 13:
        _is_empty(graph)
    # verificar se o grafo é completo
    elif opcao == 14:
        _is_complete(graph)
    # verificar se o grafo é simples
    elif opcao == 15:
        _is_simple(graph)
    # verificar conectividade do grafo
    elif opcao == 16:
        _is_connected(graph)
    # utilizar Kosaraju para calcular o número de componentes fortemente conexos
    elif opcao == 17:
        _kosaraju(graph)
    # pegar articulações
    elif opcao == 18:
        _get_articulations(graph)
    # pegar pontes
    elif opcao == 19:
        _get_bridges(graph)
    # verificar se o grafo é euleriano
    elif opcao == 20:
        _is_eulerian(graph)
    # transformar grafo em XML
    elif opcao == 21:
        _graph_to_xml(graph)
    # transformar XML em grafo
    elif opcao == 22:
        _xml_to_graph(graph)
    elif opcao == 23:
        print(graph)
    
    
def _add_node(graph: IGrafo):
    edge_name = input("Digite o nome do nó: ")
    edge_weight = None
    try:
        edge_weight = float(input("Digite o peso do nó: "))
    except ValueError:
        print("Por favor, insira um número válido.")
    
    try:
        graph.add_node(edge_name, edge_weight)
    except ValueError as e:
        print(e)
        
def _remove_node(graph: IGrafo):
    edge_name = input("Digite o nome do nó: ")
    try:
        graph.remove_node(edge_name)
    except ValueError as e:
        print(e)
        
def _add_edge(graph: IGrafo):
    predecessor = input("Digite o nó de origem: ")
    successor = input("Digite o nó de destino: ")
    edge_weight = None
    try:
        edge_weight = float(input("Digite o peso da aresta: "))
    except ValueError:
        print("Por favor, insira um número válido.")
    edge_name = input("Digite o nome da aresta: ")
    
    try:
        graph.add_edge(predecessor, successor, edge_weight, edge_name)
    except ValueError as e:
        print(e)
        
def _remove_edge_by_name(graph: IGrafo):
    edge_name = input("Digite o nome da aresta: ")
    try:
        graph.remove_edge_by_name(edge_name)
    except ValueError as e:
        print(e)
        
def _remove_all_edges_by_nodes(graph: IGrafo):
    predecessor = input("Digite o nó de origem: ")
    successor = input("Digite o nó de destino: ")
    try:
        graph.remove_all_edges_by_nodes(predecessor, successor)
    except ValueError as e:
        print(e)
        
def _thers_node_adjacency(graph: IGrafo):
    predecessor = input("Digite o nó de origem: ")
    successor = input("Digite o nó de destino: ")
    try:
        print(graph.thers_node_adjacency(predecessor, successor))
    except ValueError as e:
        print(e)

def _thers_edge_adjacency(graph: IGrafo):
    edge1 = input("Digite o nome da primeira aresta: ")
    edge2 = input("Digite o nome da segunda aresta: ")
    try:
        print(graph.thers_edge_adjacency(edge1, edge2))
    except ValueError as e:
        print(e)

def _thers_edge_by_name(graph: IGrafo):
    edge_name = input("Digite o nome da aresta: ")
    try:
        print(graph.thers_edge_by_name(edge_name))
    except ValueError as e:
        print(e)

def _thers_edge_by_nodes(graph: IGrafo):
    predecessor = input("Digite o nó de origem: ")
    successor = input("Digite o nó de destino: ")
    try:
        print(graph.thers_edge_by_nodes(predecessor, successor))
    except ValueError as e:
        print(e)

def _get_edge_count(graph: IGrafo):
    print(graph.get_edge_count())

def _get_node_count(graph: IGrafo):
    print(graph.get_node_count())

def _is_empty(graph: IGrafo):
    print(graph.is_empty())

def _is_complete(graph: IGrafo):
    print(graph.is_complete())

def _is_simple(graph: IGrafo):
    print(graph.is_simple())

def _is_connected(graph: IGrafo):
    print(graph.is_connected())

def _kosaraju(graph: IGrafo):
    print(graph.kosaraju())

def _get_articulations(graph: IGrafo):
    print(graph.get_articulations())

def _get_bridges(graph: IGrafo):
    print(graph.get_bridge())

def _is_eulerian(graph: IGrafo):
    by_tarjan = None
    while by_tarjan != "s" and by_tarjan != "n":
        by_tarjan = input("Deseja verificar se o grafo é euleriano por meio do algoritmo de Tarjan? (s/n): ").lower()
    print(graph.get_euler_path())

def _graph_to_xml(graph: IGrafo):
    print("Processando...")
    graph.to_xml()
    print("Grafo transformado em XML com sucesso.")
    
def _xml_to_graph(graph: IGrafo):
    file_path = input("Digite o caminho do arquivo XML: ")
    print("Processando...")
    graph.to_graph(file_path)
    print("XML transformado em grafo com sucesso.")