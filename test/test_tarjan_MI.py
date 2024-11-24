import unittest
from GrafoMI import GrafoMI
from datetime import datetime
import sys

# Increase the recursion limit
sys.setrecursionlimit(150000)


class TestTarjanMI(unittest.TestCase):

    def setUp(self):
        self.graphMI_with_100_nodes = GrafoMI(DIRECTED=False)
        self.graphMI_with_1000_nodes = GrafoMI(DIRECTED=False)
        self.graphMI_with_10000_nodes = GrafoMI(DIRECTED=False)
        self.graphMI_with_100000_nodes = GrafoMI(DIRECTED=False)

    def test_tarjan_with_one_hundred_nodes(self):
        self.graphMI_with_100_nodes.to_graph("output/eulerian_graph.gexf")
        print("GraphMI Gerado with 100 nodes")
        startTime = datetime.now()
        self.graphMI_with_100_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan")
        startTime = datetime.now()
        self.graphMI_with_100_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan")

    def test_tarjan_with_one_thousand_nodes(self):

        self.graphMI_with_1000_nodes.to_graph("output/eulerian_graph_1000.gexf")
        print("GraphMI Gerado with 1000 nodes de forma automatica")
        startTime = datetime.now()
        self.graphMI_with_1000_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan")
        startTime = datetime.now()
        self.graphMI_with_1000_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan")

    def test_tarjan_with_ten_thousand_nodes(self):
        self.graphMI_with_10000_nodes.to_graph("output/eulerian_graph_10000.gexf")
        print("GraphMI Gerado with 10000 nodes de forma automatica")
        startTime = datetime.now()
        self.graphMI_with_10000_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan")
        startTime = datetime.now()
        self.graphMI_with_10000_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan")

    def test_tarjan_with_one_hundred_thousand_nodes(self):
        self.graphMI_with_100000_nodes.to_graph("output/eulerian_graph_100000.gexf")
        print("GraphMI Gerado with 100000 nodes de forma automatica")
        startTime = datetime.now()
        self.graphMI_with_100000_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan")
        startTime = datetime.now()
        self.graphMI_with_100000_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan")


if __name__ == "__main__":
    unittest.main()
