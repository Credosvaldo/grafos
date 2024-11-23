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

b = GrafoMI(DIRECTED=True)
b.add_node("A", 1.0)
b.add_node("B", 1.0)
b.add_node("C", 1.0)
b.add_edge("A", "B", 1.0)
b.add_edge("A", "C", 1.0)
b.add_edge("B", "C", 1.0)
print(b.is_simple())
b.add_edge("A", "A", 1.0, "edge1")
print(b.is_simple())
b.remove_edge_by_name("edge1")
b.add_edge("B", "A", 1.0, "edge1")
print(b.is_simple())

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


graphMI = GrafoMI()
graphMI.to_graph("output/graphMI.gexf")
graphMa = GrafoMA()
graphMa.to_graph("output/graphMI.gexf")

graphLA = GrafoLA()
graphLA.to_graph("output/graphMI.gexf")


print(graphMI)
print(graphMa)
print(graphLA)


print(graphMI.is_complete())
print(graphMa.is_complete())
print(graphLA.is_complete())

print(graphMI.is_simple())
print(graphMa.is_simple())
print(graphLA.is_simple())


