import unittest
from GrafoMA import GrafoMA
from datetime import datetime
import sys


# Increase the recursion limit to the maximum possible value
sys.setrecursionlimit(922337203)


class TestTarjanMA(unittest.TestCase):

    def setUp(self):
        self.graphMA_with_100_nodes = GrafoMA(DIRECTED=False)
        self.graphMA_with_1000_nodes = GrafoMA(DIRECTED=False)
        self.graphMA_with_10000_nodes = GrafoMA(DIRECTED=False)
        self.graphMA_with_100000_nodes = GrafoMA(DIRECTED=False)

    def test_tarjan_with_one_hundred_nodes(self):
        self.graphMA_with_100_nodes.to_graph("output/eulerian_graph.gexf")
        print("GraphMA Gerado with 100 nodes")
        startTime = datetime.now()
        self.graphMA_with_100_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100 nodes")
        startTime = datetime.now()
        self.graphMA_with_100_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100 nodes")

    def test_tarjan_with_one_thousand_nodes(self):

        self.graphMA_with_1000_nodes.to_graph("output/eulerian_graph_1000.gexf")
        print("GraphMA Gerado with 1000 nodes de forma automatica")
        startTime = datetime.now()
        self.graphMA_with_1000_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 1000 nodes")
        startTime = datetime.now()
        self.graphMA_with_1000_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 100 nodes")

    def test_tarjan_with_ten_thousand_nodes(self):
        self.graphMA_with_10000_nodes.to_graph("output/eulerian_graph_10000.gexf")
        print("GraphMA Gerado with 10000 nodes de forma automatica")
        startTime = datetime.now()
        self.graphMA_with_10000_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 10000 nodes")
        startTime = datetime.now()
        self.graphMA_with_10000_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan and 10000 nodes")

    def test_tarjan_with_one_hundred_thousand_nodes(self):
        self.graphMA_with_100000_nodes.to_graph("output/eulerian_graph_100000.gexf")
        print("GraphMA Gerado with 100000 nodes de forma automatica")
        startTime = datetime.now()
        self.graphMA_with_100000_nodes.get_euler_path()
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with Tarjan and 100000 nodes")
        startTime = datetime.now()
        self.graphMA_with_100000_nodes.get_euler_path(by_tarjan=False)
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds with out Tarjan  and 100000 nodes")


if __name__ == "__main__":
    unittest.main()
