from Grafo import GrafoMA

a = GrafoMA(DIRECTED=True)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)
a.add_edge(2, 1, 6)
a.add_edge(3, 2, 5)

print(a)


a.remove_all_edge_by_vertices(3, 2)
print(a)
print(a.edges_map)
print(a.vertices_map)

a.thers_vertice_adjacente(90, 87)