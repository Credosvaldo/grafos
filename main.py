from DFSNode import DFSNode
from Grafo import GrafoMA
from GrafoLA import GrafoLA

a = GrafoMA(DIRECTED=False)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)


euler_path = a.get_euler_path()
print(euler_path)
print(a)

b = GrafoLA(DIRECTED=False)

b.add_node("1", 7)
b.add_node("2", 8)
b.add_node("3", 9)

b.add_edge("1", "2", 7, "1-2")
b.add_edge("3", "2", 8, "3-2")
b.add_edge("3", "2", 1, "3-2")
b.add_edge("3", "3", 9, "3-3")

print(b)


print(b.thers_edge_by_nodes("1", "2"))