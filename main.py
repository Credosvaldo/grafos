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


graphLa = GrafoMI()
graphLa.add_node("A", 1.0)
graphLa.add_node("B", 2.0)
graphLa.add_node("C", 3.0)
graphLa.add_node("D", 4.0)
graphLa.add_node("E", 5.0)
graphLa.add_node("F", 6.0)

graphLa.add_edge("A", "B", 1.0, "edge1")
graphLa.add_edge("A", "C", 2.0, "edge2")
graphLa.add_edge("B", "D", 3.0, "edge3")
graphLa.add_edge("B", "E", 4.0, "edge4")
graphLa.add_edge("C", "F", 5.0, "edge5")
graphLa.add_edge("D", "F", 6.0, "edge6")
graphLa.add_edge("E", "F", 7.0, "edge7")

graphLa.to_xml()

graphMa = GrafoMA()
graphMa.to_graph("output/graphMI.gexf")

graphMI = GrafoLA()
graphMI.to_graph("output/graphMI.gexf")


print(graphLa)
print(graphMa)
print(graphMI)







# a = GrafoMA(DIRECTED=True)

# a.add_edge(1, 2, 1)
# a.add_edge(2, 5, 1)
# a.add_edge(5, 3, 1)
# a.add_edge(3, 1, 1)

# a.add_edge(1, 4, 1)
# a.add_edge(4, 6, 1)
# a.add_edge(3, 6, 1)

# a.add_edge(5, 7, 1)
# a.add_edge(6, 7, 1)
# a.add_edge(7, 6, 1)

# print(a)
# print(a.kosaraju())