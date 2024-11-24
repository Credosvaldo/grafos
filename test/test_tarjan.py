from sqlite3 import Time
import unittest
from GrafoLA import GrafoLA
from GrafoMA import GrafoMA
from GrafoMI import GrafoMI


class TestTarjan(unittest.TestCase):

    def setUp(self):
        self.graphLA = GrafoLA(DIRECTED=False)
        self.graphMA = GrafoMA(DIRECTED=False)
        self.graphMI = GrafoMI(DIRECTED=False)

    def test_tarjan_with_one_hundred_nodes(self):
        self.graphMA = GrafoMA(
            DIRECTED=False, num_nodes=100, random_graph_generation=True
        )
        startTime = Time.time()
        print(self.graphMA.get_euler_path())
        endTime = Time.time()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds")

        startTime = Time.time()
        print(self.graphMA.get_euler_path(by_tarjan=False))
        endTime = Time.time()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds")
        
        


if __name__ == "__main__":
    unittest.main()
