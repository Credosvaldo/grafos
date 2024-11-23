import unittest

from GrafoMI import GrafoMI
from enums.ConnectivityDegree import ConnectivityDegree


class TestGrafoMI(unittest.TestCase):

    def setUp(self):
        self.graph = GrafoMI(DIRECTED=True)

    def test_kosaraju_single_node(self):
        self.graph.add_node("A")
        self.assertEqual(self.graph.kosaraju(), 1)

    def test_kosaraju_disconnected_nodes(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.assertEqual(self.graph.kosaraju(), 2)

    def test_kosaraju_connected_nodes(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.assertEqual(self.graph.kosaraju(), 2)

    def test_kosaraju_strongly_connected(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "A")
        self.assertEqual(self.graph.kosaraju(), 1)

    def test_kosaraju_multiple_components(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "A")
        self.graph.add_edge("C", "A")
        self.assertEqual(self.graph.kosaraju(), 2)

    def test_kosaraju_complex_graph(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_node("D")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.graph.add_edge("C", "A")
        self.graph.add_edge("C", "D")
        self.assertEqual(self.graph.kosaraju(), 2)

    def test_add_node(self):
        self.graph.add_node("A")
        self.assertEqual(self.graph.get_node_count(), 1)
        self.assertTrue("A" in self.graph.nodes_map)

    def test_add_edge(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 2.5, "edge1")
        self.assertEqual(self.graph.get_edge_count(), 1)
        self.assertTrue("edge1" in self.graph.edges_map)

    def test_remove_node(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 2.5, "edge1")
        self.graph.remove_node("A")
        self.assertEqual(self.graph.get_node_count(), 1)
        self.assertFalse("A" in self.graph.nodes_map)
        self.assertEqual(self.graph.get_edge_count(), 0)

    def test_remove_edge_by_name(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 2.5, "edge1")
        self.graph.remove_edge_by_name("edge1")
        self.assertEqual(self.graph.get_edge_count(), 0)
        self.assertFalse("edge1" in self.graph.edges_map)

    def test_is_empty(self):
        self.assertTrue(self.graph.is_empty())
        self.graph.add_node("A")
        self.assertFalse(self.graph.is_empty())

    def test_is_complete(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.assertFalse(self.graph.is_complete())
        self.graph.add_edge("B", "A")
        self.assertTrue(self.graph.is_complete())

    def test_is_simple(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.assertTrue(self.graph.is_simple())
        self.graph.add_edge("A", "B", name="edge2")
        self.assertFalse(self.graph.is_simple())

    def test_get_all_nodes_degree(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        degrees = self.graph.get_all_nodes_degree()
        self.assertEqual(degrees["A"], 1)
        self.assertEqual(degrees["B"], 1)

    def test_get_edges_by_node(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", name="edge1")
        edges = self.graph.get_edges_by_node("A")
        self.assertEqual(edges, ["edge1"])

    def test_is_bridge(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", name="edge1")
        self.assertTrue(self.graph.is_brige("edge1"))

    def test_get_euler_path(self):
        self.graph = GrafoMI(DIRECTED=False)
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        self.graph.add_edge("C", "A")
        euler_path = self.graph.get_euler_path()
        self.assertEqual(len(euler_path), 4)
        self.assertEqual(euler_path[0], euler_path[-1])

    def test_get_articulations(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "C")
        articulations = self.graph.get_articulations()
        self.assertEqual(articulations, ["B"])

    def test_get_bridge(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_node("C")
        self.graph.add_edge("A", "B", name="edge1")
        self.graph.add_edge("B", "C", name="edge2")
        bridges = self.graph.get_bridge()
        self.assertEqual(bridges, ["edge1", "edge2"])

    def test_is_connected(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.assertTrue(self.graph.is_connected())
        self.graph.remove_edge_by_name("edge1")
        self.assertFalse(self.graph.is_connected())

    def test_connectivity_degree(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.assertEqual(
            self.graph.connectivity_degree(),
            ConnectivityDegree.UNIDIRECTIONAL_CONNECTED,
        )
        self.graph.add_edge("B", "A")
        self.assertEqual(
            self.graph.connectivity_degree(), ConnectivityDegree.STRONGLY_CONNECTED
        )

    def test_make_revert_graph(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        revert_graph = self.graph.make_revert_graph()
        self.assertTrue(revert_graph.thers_edge_by_nodes("B", "A"))
        self.assertFalse(revert_graph.thers_edge_by_nodes("A", "B"))

    def test_make_underlying_graph(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        underlying_graph = self.graph.make_underlying_graph()
        self.assertTrue(underlying_graph.thers_edge_by_nodes("A", "B"))
        self.assertTrue(underlying_graph.thers_edge_by_nodes("B", "A"))

    def test_to_graph(self):
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B")
        self.graph.add_edge("B", "A")
        self.graph.to_xml()
        self.graph.to_graph("output/graphMI.gexf")
        self.assertEqual(self.graph.get_node_count(), 2)
        self.assertEqual(self.graph.get_edge_count(), 2)


if __name__ == "__main__":
    unittest.main()
