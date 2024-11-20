from DFSNode import DFSNode
from Grafo import GrafoMA
from GrafoLA import GrafoLA

a = GrafoMA(DIRECTED=True)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)
a.add_edge(2, 1, 6)
a.add_edge(3, 2, 5)

print(a)

b = GrafoLA(DIRECTED=True)

b.add_node("1", 7)
b.add_node("2", 8)
b.add_node("3", 9)

b.add_edge("1", "2", 7, "1-2")
b.add_edge("3", "2", 8, "3-2")
b.add_edge("3", "2", 1, "3-2-b")
b.add_edge("3", "3", 9, "3-3")
b.add_edge("2", "1", 9, "2-1")
b.add_edge("3", "1", 9, "3-1")
b.add_edge("1", "3", 9, "1-3")
b.add_edge("3", "1", 9, "3-1-b")
print(b)


print(b.thers_edge_by_nodes("1", "2"))
print(b.is_empty())
print(b.get_edge_count())
print(b.isComplete())
print(b.is_simple())

c  = GrafoLA(DIRECTED=True, num_nodes=12)

print(c.is_simple())
