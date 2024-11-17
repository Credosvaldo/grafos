from Grafo import GrafoMA

a = GrafoMA(DIRECTED=True)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)
a.add_edge(2, 1, 6)
a.add_edge(3, 2, 5)

print(a)
print(a.vertices_map)
print(a.edges_map)


a.remove_vertice(2)

print(a)
a.add_vertice(9)
#a.add_edge(4, 3, 3)

print(a)
print(a.vertices_map)
print(a.edges_map)