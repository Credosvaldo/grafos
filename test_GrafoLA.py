import unittest
from GrafoLA import GrafoLA
from NodeLA import NodeLA

class TestGrafoLA(unittest.TestCase):

    def setUp(self):
        self.graph = GrafoLA(DIRECTED=True)

    def test_add_node(self):
        self.graph.add_node("A", 1.0)
        self.assertIn("A", self.graph.nodes_map)
        self.assertEqual(self.graph.nodes_map["A"].weight, 1.0)

    def test_remove_node(self):
        self.graph.add_node("A", 1.0)
        self.graph.remove_node("A")
        self.assertNotIn("A", self.graph.nodes_map)

    def test_add_edge(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertIn("edge1", self.graph.edges_map)
        self.assertEqual(self.graph.edges_map["edge1"], ("A", "B", 3.0))

    def test_remove_edge_by_name(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.graph.remove_edge_by_name("edge1")
        self.assertNotIn("edge1", self.graph.edges_map)

    def test_is_empty(self):
        self.assertTrue(self.graph.is_empty())
        self.graph.add_node("A", 1.0)
        self.assertFalse(self.graph.is_empty())

    def test_get_edge_count(self):
        self.assertEqual(self.graph.get_edge_count(), 0)
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graph.get_edge_count(), 1)

    def test_get_node_count(self):
        self.assertEqual(self.graph.get_node_count(), 0)
        self.graph.add_node("A", 1.0)
        self.assertEqual(self.graph.get_node_count(), 1)

    def test_is_connected(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graph.is_connected())

    def test_is_complete(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.graph.add_edge("B", "A", 3.0, "edge2")
        self.assertTrue(self.graph.is_complete())

    def test_is_simple(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graph.is_simple())

    def test_get_bridge(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graph.get_bridge(), ["edge1"])

    def test_get_articulations(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graph.get_articulations(), ["A", "B"])

if __name__ == '__main__':
    unittest.main()