from models.DFSNode import DFSNode
from GrafoMA import GrafoMA
from GrafoLA import GrafoLA

a = GrafoMA(DIRECTED=False)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)

d = GrafoLA(DIRECTED=False)
d.add_edge(1, 2, 7)
d.add_edge(3, 2, 8)
d.add_edge(3, 1, 9)


e = GrafoLA().to_graph("output/graphLA.gexf")
f = GrafoMA().to_graph("output/graphMA.gexf")

print(a)
print(f)

print(d)
print(e)


euler_a = a.get_euler_path()
euler_d = d.get_euler_path()

print(euler_a)
print(euler_d)

graph = GrafoLA()
graph.DIRECTED = True
graph.add_node("A", 1.0)
graph.add_node("B", 2.0)
graph.add_edge("A", "B", 3.0, "edge1")
graph.add_edge("B", "AC", 3.0, "edge2")

print(graph)
graph.print_revert_graph()