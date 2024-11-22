from models.DFSNode import DFSNode
from GrafoMA import GrafoMA
from GrafoLA import GrafoLA
from GrafoMI import GrafoMI

a = GrafoMA(DIRECTED=False)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)

d = GrafoLA(DIRECTED=False)
d.add_edge(1, 2, 7)
d.add_edge(3, 2, 8)
d.add_edge(3, 1, 9)

b = GrafoMI(DIRECTED=False)
b.add_edge(1, 2, 7)
b.add_edge(3, 2, 8)
b.add_edge(3, 1, 9)
b.add_node("A", 1.0)
b.add_node("B", 1.0)
b.add_edge("A", "B", 1.0, "edge1")
b.remove_edge_by_name("edge1")
b.add_edge("A", "B", 1.0, "edge1")
b.add_edge("B", "A", 1.0, "edge2")
b.remove_node("A")
print(b.thers_node_adjacente("B", "1"))
print(b.thers_node_adjacente("1", "2")) 
print(b.thers_node_adjacente("2", "1"))


e = GrafoLA().to_graph("output/graphLA.gexf")
f = GrafoMA().to_graph("output/graphMA.gexf")

print(a)
print(f)
print(b)
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