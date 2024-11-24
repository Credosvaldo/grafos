from GrafoLA import GrafoLA
from GrafoMA import GrafoMA
from GrafoMI import GrafoMI


graph = GrafoLA(DIRECTED=False)

graph.add_edge(0, 1)
graph.add_edge(0, 2)
graph.add_edge(0, 3)


graph.add_edge(1, 2)
graph.add_edge(1, 3)

graph.add_edge(2, 3)

print(graph)

graph.to_xml("output/eulerian_graph_5.gexf")

graph = GrafoMA()
graph.to_graph("output/eulerian_graph_5.gexf")
print(graph)


graph = GrafoMI(DIRECTED=False)
graph.to_graph("output/eulerian_graph_5.gexf")
print(graph)
