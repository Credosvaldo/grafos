import unittest
from GrafoLA import GrafoLA


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
        self.graph.add_node("C", 3.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.graph.add_edge("B", "C", 3.0, "edge2")

        self.assertEqual(self.graph.get_articulations(), ["B"])

    def test_thers_node_adjacency(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graph.thers_node_adjacency("A", "B"))
        self.assertFalse(self.graph.thers_node_adjacency("B", "A"))

    def test_thers_edge_by_name(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graph.thers_edge_by_name("edge1"))
        self.assertFalse(self.graph.thers_edge_by_name("edge2"))

    def test_thers_edge_by_nodes(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graph.thers_edge_by_nodes("A", "B"))
        self.assertFalse(self.graph.thers_edge_by_nodes("B", "A"))

    def test_thers_edge_adjacency(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_node("C", 3.0)
        self.graph.add_node("D", 4.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.graph.add_edge("B", "A", 3.0, "edge2")
        self.graph.add_edge("D", "C", 3.0, "edge3")
        self.assertTrue(self.graph.thers_edge_adjacency("edge1", "edge2"))
        self.assertFalse(self.graph.thers_edge_adjacency("edge1", "edge3"))

    def test_get_all_nodes_degree(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graph.get_all_nodes_degree(), {"A": 1, "B": 0})

    def test_get_euler_path(self):
        self.graph.DIRECTED = False
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")

        euler_path = self.graph.get_euler_path()
        self.assertEqual(euler_path, ["A", "B"])

    def test_is_bridget(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graph.is_bridget("edge1"))

    def test_is_articulation(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.graph.add_node("C", 3.0)
        self.graph.add_edge("B", "C", 4.0, "edge2")
        self.assertTrue(self.graph.is_articulation("B"))

    def test_make_underlying_graph(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        underlying_graph = self.graph.make_underlying_graph()
        self.assertFalse(underlying_graph.DIRECTED)
        self.assertIn("A", underlying_graph.nodes_map)
        self.assertIn("B", underlying_graph.nodes_map)
        self.assertIn("edge1", underlying_graph.edges_map)

    def test_get_bridges(self):
        self.graph.add_node("A", 1.0)
        self.graph.add_node("B", 2.0)
        self.graph.add_node("C", 3.0)
        self.graph.add_edge("A", "B", 3.0, "edge1")
        self.graph.add_edge("B", "C", 3.0, "edge2")
        self.assertEqual(self.graph.get_bridge(), ["edge1", "edge2"])


if __name__ == "__main__":
    unittest.main()
