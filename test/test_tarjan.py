import unittest
from GrafoLA import GrafoLA
from GrafoMA import GrafoMA
from GrafoMI import GrafoMI
from datetime import datetime
import sys

# Increase the recursion limit
sys.setrecursionlimit(150000)


class TestTarjan(unittest.TestCase):

    def setUp(self):
        self.graphLA = GrafoLA(DIRECTED=False)
        self.graphMA = GrafoMA(DIRECTED=False)
        self.graphMI = GrafoMI(DIRECTED=False)

    def test_tarjan_with_one_hundred_nodes(self):
        self.graphMA.gra(self.graphLA)

        print("GrafoMA Gerado")
        print(self.graphMA)
        print(self.graphMA.get_euler_path())
        startTime = datetime.now()
        print(self.graphMA.get_euler_path())
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds")

        startTime = datetime.now()
        print(self.graphMA.get_euler_path(by_tarjan=False))
        endTime = datetime.now()
        elapsedTime = endTime - startTime
        print(f"Elapsed time: {elapsedTime} seconds")


if __name__ == "__main__":
    unittest.main()
