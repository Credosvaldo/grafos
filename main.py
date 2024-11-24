from models.DFSNode import DFSNode
from GrafoMA import GrafoMA
from GrafoLA import GrafoLA
from GrafoMI import GrafoMI
import sys
from datetime import datetime

sys.setrecursionlimit(922337203)

# Lista de adjacencia

# graphLA_with_100_nodes = GrafoLA(DIRECTED=False)
# graphLA_with_100_nodes.to_graph("output/eulerian_graph.gexf")
# print("GraphLA Gerado with 100 nodes")
# startTime = datetime.now()
# graphLA_with_100_nodes.get_euler_path()
# endTime = datetime.now()
# elapsedTime = endTime - startTime
# print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100 nodes")
# startTime = datetime.now()
# graphLA_with_100_nodes.get_euler_path(by_tarjan=False)
# endTime = datetime.now()
# elapsedTime = endTime - startTime
# print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100 nodes")

# graphLA_with_1000_nodes = GrafoLA(DIRECTED=False)
# graphLA_with_1000_nodes.to_graph("output/eulerian_graph_1000.gexf")
# print("GraphLA Gerado with 1000 nodes de forma automatica")
# startTime = datetime.now()
# graphLA_with_1000_nodes.get_euler_path()
# endTime = datetime.now()
# elapsedTime = endTime - startTime
# print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 1000 nodes")
# startTime = datetime.now()
# graphLA_with_1000_nodes.get_euler_path(by_tarjan=False)
# endTime = datetime.now()
# elapsedTime = endTime - startTime
# print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 1000 nodes")


# graphLA_with_10000_nodes = GrafoLA(DIRECTED=False)
# graphLA_with_10000_nodes.to_graph("output/eulerian_graph_10000.gexf")
# print("GraphLA Gerado with 10000 nodes de forma automatica")
# startTime = datetime.now()
# graphLA_with_10000_nodes.get_euler_path()
# endTime = datetime.now()
# elapsedTime = endTime - startTime
# print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 10000 nodes")
# startTime = datetime.now()
# graphLA_with_10000_nodes.get_euler_path(by_tarjan=False)
# endTime = datetime.now()
# elapsedTime = endTime - startTime
# print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 10000 nodes")

graphLA_with_100000_nodes = GrafoLA(DIRECTED=False, num_nodes=100000, random_graph_generation=True)
graphLA_with_100000_nodes.to_xml("output/eulerian_graph_100000.xml")
print("GraphLA Gerado with 100000 nodes de forma automatica")
startTime = datetime.now()
graphLA_with_100000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100000 nodes")
startTime = datetime.now()
graphLA_with_100000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100000 nodes")


# Matrix de adjacencia
graphMA_with_100_nodes = GrafoMA(DIRECTED=False)
graphMA_with_100_nodes.to_graph("output/eulerian_graph.gexf")
print("GraphMA Gerado with 100 nodes")
startTime = datetime.now()
graphMA_with_100_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100 nodes")
startTime = datetime.now()
graphMA_with_100_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100 nodes")

graphMA_with_1000_nodes = GrafoMA(DIRECTED=False)
graphMA_with_1000_nodes.to_graph("output/eulerian_graph_1000.gexf")
print("GraphMA Gerado with 1000 nodes de forma automatica")
startTime = datetime.now()
graphMA_with_1000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 1000 nodes")
startTime = datetime.now()
graphMA_with_1000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 1000 nodes")

graphMA_with_10000_nodes = GrafoMA(DIRECTED=False)
graphMA_with_10000_nodes.to_graph("output/eulerian_graph_10000.gexf")
print("GraphMA Gerado with 10000 nodes de forma automatica")
startTime = datetime.now()
graphMA_with_10000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 10000 nodes")
startTime = datetime.now()
graphMA_with_10000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 10000 nodes")

graphMA_with_100000_nodes = GrafoMA(DIRECTED=False)
graphMA_with_100000_nodes.to_graph("output/eulerian_graph_100000.gexf")
print("GraphMA Gerado with 100000 nodes de forma automatica")
startTime = datetime.now()
graphMA_with_100000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100000 nodes")
startTime = datetime.now()
graphMA_with_100000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100000 nodes")


## Matrix de Incidencia

graphMI_with_100_nodes = GrafoMI(DIRECTED=False)
graphMI_with_100_nodes.to_graph("output/eulerian_graph.gexf")
print("GraphMI Gerado with 100 nodes")
startTime = datetime.now()
graphMI_with_100_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100 nodes")
startTime = datetime.now()
graphMI_with_100_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100 nodes")

graphMI_with_1000_nodes = GrafoMI(DIRECTED=False)
graphMI_with_1000_nodes.to_graph("output/eulerian_graph_1000.gexf")
print("GraphMI Gerado with 1000 nodes de forma automatica")
startTime = datetime.now()
graphMI_with_1000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 1000 nodes")
startTime = datetime.now()
graphMI_with_1000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 1000 nodes")

graphMI_with_10000_nodes = GrafoMI(DIRECTED=False)
graphMI_with_10000_nodes.to_graph("output/eulerian_graph_10000.gexf")
print("GraphMI Gerado with 10000 nodes de forma automatica")
startTime = datetime.now()
graphMI_with_10000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 10000 nodes")
startTime = datetime.now()
graphMI_with_10000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 10000 nodes")

graphMI_with_100000_nodes = GrafoMI(DIRECTED=False)
graphMI_with_100000_nodes.to_graph("output/eulerian_graph_100000.gexf")
print("GraphMI Gerado with 100000 nodes de forma automatica")
startTime = datetime.now()
graphMI_with_100000_nodes.get_euler_path()
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100000 nodes")
startTime = datetime.now()
graphMI_with_100000_nodes.get_euler_path(by_tarjan=False)
endTime = datetime.now()
elapsedTime = endTime - startTime
print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100000 nodes")
