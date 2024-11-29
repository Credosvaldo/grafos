from models.DFSNode import DFSNode
from GrafoMA import GrafoMA
from GrafoLA import GrafoLA
from GrafoMI import GrafoMI
import sys
from datetime import datetime

a = GrafoMA(DIRECTED=True, num_nodes=5, num_edges=10, ramdom_graph_shold_be_simple=False)
b = GrafoMA(DIRECTED=True, num_nodes=5, ramdom_graph_shold_be_linear=True)

print(b)

exit()

a = GrafoMA(DIRECTED=False)

a.add_node("A")

a.add_edge("A", "B", 5)
a.add_edge("A", "C", -3)
a.add_edge("B", "C", 2)

print(a)
print('Grafo a é completo: ', a.is_complete())
a.add_node("D", 2)
print('Grafo a é completo: ', a.is_complete())
a.remove_node("D")
print('Caminho euleriano grafo a: ', a.get_euler_path())
a.add_edge("A", "A", name='aresta')
print(a)
print('Grafo a é simples: ', a.is_simple())
a.remove_edge_by_name('aresta')
a.to_xml()


b = GrafoMI(DIRECTED=False)
b.to_graph('output/graphMA.gexf')
print(b)


c = GrafoLA(DIRECTED=True)
c.add_edge("A", "B")
c.add_edge("A", "C")
print(c)
print('Grau de conectividade grafo c: ', c.connectivity_degree())
c.add_edge("B", "C")
c.add_edge("C", "A")
print('Grau de conectividade grafo c: ', c.connectivity_degree())
