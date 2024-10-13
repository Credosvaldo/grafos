from GrafoMA import GrafoMA


a = GrafoMA(DIRECTED=False, num_vertices=3)

a.add_edge(1,2)
a.add_edge(1,2, 7)
a.add_edge(1,2, 'a')
print(a)
a.add_vertice()
a.add_vertice('P')
print("\n")
print(a)

print()
print(a.vertices_map)