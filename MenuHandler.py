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