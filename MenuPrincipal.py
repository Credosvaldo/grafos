from GrafoMA import GrafoMA
from GrafoLA import GrafoLA
from GrafoMI import GrafoMI
from IGrafo import IGrafo
from typing import Type
from MenuHandler import options_switch
import sys

def print_opcoes_grafos(graph: IGrafo):
    print("\nMenu de Opções")
    print("=" * 50)
    print("1 - Adicionar Nó")
    print("2 - Remover Nó")
    print("3 - Adicionar Aresta")
    print("4 - Remover Aresta pelo nome")
    print("5 - Remover Aresta por nós")
    print("6 - Verificar adjacência entre nós")
    print("7 - Verificar se há apenas uma aresta entre dois nós")
    print("8 - Verificar adjacência entre arestas")
    print("9 - Verificar se há aresta pelo nome")
    print("10 - Verificar se há aresta entre nós")
    print("11 - Contar arestas")
    print("12 - Contar nós")
    print("13 - Verificar se o grafo está vazio")
    print("14 - Verificar se o grafo é completo")
    print("15 - Verificar se o grafo é simples")
    print("16 - Verificar conectividade do grafo")
    print("17 - Utilizar Kosaraju para calcular o número de componentes fortemente conexos")
    print("18 - Pegar articulações")
    print("19 - Pegar pontes")
    print("20 - Verificar se o grafo é euleriano")
    print("21 - Transformar grafo em XML")
    print("22 - Transformar XML em grafo")
    print("0 - Sair")
    
    
def main_menu():
    print("TRABALHO FINAL - TEORIA DOS GRAFOS E COMPUTABILIDADE\n")
    print("Menu Inicial")
    print("=" * 50)
    
    directed = None
    graph_choice = None
    random_graph = None
    nodes = None
    edges = None
    grafo_linear = None
    
    while directed not in [1, 2]:
        try:
            directed = int(input("O grafo será direcionado? (1 - Sim, 2 - Não): "))
        except ValueError:
            print("Por favor, insira um número válido.")
    directed = directed == 1
    
    while graph_choice not in [1, 2, 3]:
        try:
            print("\nEscolha a representação a ser usada:")
            print("1 - Matriz de Adjacência")
            print("2 - Matriz de Incidência")
            print("3 - Lista de Adjacência")
            graph_choice = int(input("Digite sua escolha: "))
        except ValueError:
            print("Por favor, insira um número válido.")
            
    while random_graph not in ['y', 'n']:
        random_graph = input("\nDeseja criar um grafo aleatório? (y - Sim, n - Não): ").lower()
    
    if random_graph == 'y':
        while nodes is None or nodes < 1:
            try:
                nodes = int(input("Quantos nós deseja?: "))
            except ValueError:
                print("Por favor, insira um número válido.")
        while edges is None or edges < 1:
            try:
                edges = int(input("Quantas arestas deseja?: "))
            except ValueError:
                print("Por favor, insira um número válido.")
        
        while grafo_linear not in ['y', 'n']:
            grafo_linear = input("\nDeseja que o grafo seja linear? (y - Sim, n - Não): ").lower()
    grafo_linear = grafo_linear == 'y'
    
    graph: Type[IGrafo]
    if graph_choice == 1:
        graph = GrafoMA(DIRECTED=directed, num_nodes=nodes or 0, num_edges=edges or 0, ramdom_graph_shold_be_linear=grafo_linear)
    elif graph_choice == 2:
        graph = GrafoMI(DIRECTED=directed, num_nodes=nodes or 0, num_edges=edges or 0, ramdom_graph_shold_be_linear=grafo_linear)
    else:
        graph = GrafoLA(DIRECTED=directed, num_nodes=nodes or 0, num_edges=edges or 0, ramdom_graph_shold_be_linear=grafo_linear)

    print("=" * 50)
    while True:
        print_opcoes_grafos(graph)
        opcao = None
        try:
            opcao = int(input("\nDigite sua escolha: "))
            if opcao < 0 or opcao > 22:
                print("Por favor, insira um número válido.")
                continue
            elif opcao == 0:
                sys.exit()
            else:
                options_switch(opcao, graph)
                
        except ValueError:
            print("Por favor, insira um número válido.")