from ConvertXml import ConvertXml
from models.DFSNode import DFSNode
from GrafoMA import GrafoMA
from GrafoLA import GrafoLA
from enums.GraphType import GraphType

a = GrafoMA(DIRECTED=False)

a.add_edge(1, 2, 7)
a.add_edge(3, 2, 8)
a.add_edge(3, 1, 9)

d = GrafoLA(DIRECTED=False)
d.add_edge(1, 2, 7)
d.add_edge(3, 2, 8)
d.add_edge(3, 1, 9)

a.to_xml()
euler_path_a = a.get_euler_path()
print(euler_path_a)
euler_path_b = d.get_euler_path()
print(euler_path_b)
# b = GrafoLA(DIRECTED=True)

# b.add_node("1", 7)
# b.add_node("2", 8)
# b.add_node("3", 9)

# b.add_edge("1", "2", 7, "1-2")
# b.add_edge("3", "2", 8, "3-2")
# b.add_edge("3", "2", 1, "3-2-b")
# b.add_edge("3", "3", 9, "3-3")
# b.add_edge("2", "1", 9, "2-1")
# b.add_edge("3", "1", 9, "3-1")
# b.add_edge("1", "3", 9, "1-3")
# b.add_edge("3", "1", 9, "3-1-b")
# print(b)

# b.remove_all_edge_by_nodes("3", "2")
# print(b)

# print(b.thers_edge_by_nodes("1", "2"))
# print(b.is_empty())
# print(b.get_edge_count())
# print(b.is_complete())
# print(b.is_simple())

# c = GrafoLA(DIRECTED=True, num_nodes=12)
# b.to_xml()
# # print(c.is_simple())

# # d = ConvertXml().to_graph(graphType=GraphType.MATRIX_ADJACENCY, path="graph.gexf")

# # print(d)

# # d = ConvertXml().to_graph(graphType=GraphType.LIST_ADJACENCY, path="graph.gexf")

# # print(d)
