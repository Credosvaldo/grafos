from Grafo import GrafoMA

a = GrafoMA(DIRECTED=False)


a.add_vertice()
a.add_vertice()
a.add_vertice()
print(a)

a.add_edge(1, 2, 5, 'a')


print(a)
print(a.edges_map)
