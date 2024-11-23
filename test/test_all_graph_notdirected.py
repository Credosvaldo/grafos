import unittest
from GrafoLA import GrafoLA
from GrafoMA import GrafoMA
from GrafoMI import GrafoMI


class TestAllGraphNotDirected(unittest.TestCase):

    def setUp(self):
        self.graphLA = GrafoLA(DIRECTED=False)
        self.graphMA = GrafoMA(DIRECTED=False)
        self.graphMI = GrafoMI(DIRECTED=False)

    def test_add_edge(self):
        self.graphLA.add_edge(1, 2, 7)
        self.graphMA.add_edge(1, 2, 7)
        self.graphMI.add_edge(1, 2, 7)
        self.assertEqual(self.graphLA.get_edge_count(), self.graphMA.get_edge_count())
        self.assertEqual(self.graphLA.get_edge_count(), self.graphMI.get_edge_count())

    def test_add_node(self):
        self.graphLA.add_node(1, 7)
        self.graphMA.add_node(1, 7)
        self.graphMI.add_node(1, 7)
        self.assertEqual(self.graphLA.get_node_count(), self.graphMA.get_node_count())
        self.assertEqual(self.graphLA.get_node_count(), self.graphMI.get_node_count())

    def test_remove_edge(self):
        self.graphLA.add_edge(1, 2, 7)
        self.graphMA.add_edge(1, 2, 7)
        self.graphMI.add_edge(1, 2, 7)
        self.graphLA.remove_all_edge_by_nodes(1, 2)
        self.graphMA.remove_all_edge_by_nodes(1, 2)
        self.graphMI.remove_all_edges_by_nodes(1, 2)
        self.assertEqual(self.graphLA.get_edge_count(), self.graphMA.get_edge_count())
        self.assertEqual(self.graphLA.get_edge_count(), self.graphMI.get_edge_count())

    def test_remove_node(self):
        self.graphLA.add_node(1, 7)
        self.graphMA.add_node(1, 7)
        self.graphMI.add_node(1, 7)
        self.graphLA.remove_node(1)
        self.graphMA.remove_node(1)
        self.graphMI.remove_node(1)
        self.assertEqual(self.graphLA.get_node_count(), self.graphMA.get_node_count())
        self.assertEqual(self.graphLA.get_node_count(), self.graphMI.get_node_count())

    def test_is_simple(self):
        self.graphLA.add_node(1, 7)
        self.graphMA.add_node(1, 7)
        self.graphMI.add_node(1, 7)
        self.graphLA.add_node(2, 7)
        self.graphMA.add_node(2, 7)
        self.graphMI.add_node(2, 7)
        self.graphLA.add_edge(1, 2, 7)
        self.graphMA.add_edge(1, 2, 7)
        self.graphMI.add_edge(1, 2, 7)
        self.assertTrue(self.graphLA.is_simple())
        self.assertTrue(self.graphMA.is_simple())
        self.assertTrue(self.graphMI.is_simple())
        self.graphLA.add_edge(1, 2, 7)
        self.graphMA.add_edge(1, 2, 7)
        self.graphMI.add_edge(1, 2, 7)
        self.assertFalse(self.graphLA.is_simple())
        self.assertFalse(self.graphMA.is_simple())
        self.assertFalse(self.graphMI.is_simple())

    def test_get_euler_path(self):
        self.graphLA.add_node(1, 7)
        self.graphMA.add_node(1, 7)
        self.graphMI.add_node(1, 7)
        self.graphLA.add_node(2, 7)
        self.graphMA.add_node(2, 7)
        self.graphMI.add_node(2, 7)
        self.graphLA.add_edge(1, 2, 7)
        self.graphMA.add_edge(1, 2, 7)
        self.graphMI.add_edge(1, 2, 7)
        self.assertEqual(self.graphLA.get_euler_path(), self.graphMA.get_euler_path())
        self.assertEqual(self.graphMA.get_euler_path(), self.graphMI.get_euler_path())
    
    
    def test_tarjan(self):
        a = GrafoMA(DIRECTED=False)
        a.add_edge(1, 2, 7)
        a.add_edge(2, 3, 7)
        a.add_edge(2, 5, 7)
        a.add_edge(3, 4, 7)
        a.add_edge(3, 6, 7)
        a.add_edge(7, 4, 7)
        a.add_edge(7, 6, 7)
        a.add_edge(4, 6, 7)
        print(a)
        print(a.get_bridge_by_tarjan())


if __name__ == "__main__":
    unittest.main()
