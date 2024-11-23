import unittest
from GrafoLA import GrafoLA
from GrafoMA import GrafoMA
from GrafoMI import GrafoMI


class TestAllGraphDirected(unittest.TestCase):

    def setUp(self):
        self.graphLA = GrafoLA(DIRECTED=True)
        self.graphMA = GrafoMA(DIRECTED=True)
        self.graphMI = GrafoMI(DIRECTED=True)

    def test_add_node(self):
        self.graphLA.add_node("A", 1.0)
        self.assertIn("A", self.graphLA.nodes_map)
        self.assertEqual(self.graphLA.nodes_map["A"].weight, 1.0)

        self.graphMA.add_node("A", 1.0)
        self.assertIn("A", self.graphMA.nodes_map)
        self.assertEqual(self.graphMA.nodes_map["A"].weight, 1.0)

        self.graphMI.add_node("A", 1.0)
        self.assertIn("A", self.graphMI.nodes_map)
        self.assertEqual(self.graphMI.nodes_map["A"].weight, 1.0)

    def test_remove_node(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.remove_node("A")
        self.assertNotIn("A", self.graphLA.nodes_map)

        self.graphMA.add_node("A", 1.0)
        self.graphMA.remove_node("A")
        self.assertNotIn("A", self.graphMA.nodes_map)

        self.graphMI.add_node("A", 1.0)
        self.graphMI.remove_node("A")
        self.assertNotIn("A", self.graphMI.nodes_map)

    def test_add_edge(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertIn("edge1", self.graphLA.edges_map)
        self.assertEqual(self.graphLA.edges_map["edge1"], ("A", "B", 3.0))

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertIn("edge1", self.graphMA.edges_map)
        self.assertEqual(
            self.graphMA.edges_map["edge1"], ("A", "B", 0)
        )  # 0 is the index of the edge

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertIn("edge1", self.graphMI.edges_map)
        self.assertEqual(
            self.graphMI.edges_map["edge1"], ("A", "B", 0, 3.0)
        )  # 0 is the index of the edgecl

    def test_remove_edge_by_name(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.graphLA.remove_edge_by_name("edge1")
        self.assertNotIn("edge1", self.graphLA.edges_map)

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.graphMA.remove_edge_by_name("edge1")
        self.assertNotIn("edge1", self.graphMA.edges_map)

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.graphMI.remove_edge_by_name("edge1")
        self.assertNotIn("edge1", self.graphMI.edges_map)

    def test_is_empty(self):
        self.assertTrue(self.graphLA.is_empty())
        self.graphLA.add_node("A", 1.0)
        self.assertFalse(self.graphLA.is_empty())

        self.assertTrue(self.graphMA.is_empty())
        self.graphMA.add_node("A", 1.0)
        self.assertFalse(self.graphMA.is_empty())

        self.assertTrue(self.graphMI.is_empty())
        self.graphMI.add_node("A", 1.0)
        self.assertFalse(self.graphMI.is_empty())

    def test_get_edge_count(self):
        self.assertEqual(self.graphLA.get_edge_count(), 0)
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphLA.get_edge_count(), 1)

        self.assertEqual(self.graphMA.get_edge_count(), 0)
        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphMA.get_edge_count(), 1)

        self.assertEqual(self.graphMI.get_edge_count(), 0)
        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphMI.get_edge_count(), 1)

    def test_get_node_count(self):
        self.assertEqual(self.graphLA.get_node_count(), 0)
        self.graphLA.add_node("A", 1.0)
        self.assertEqual(self.graphLA.get_node_count(), 1)

        self.assertEqual(self.graphMA.get_node_count(), 0)
        self.graphMA.add_node("A", 1.0)
        self.assertEqual(self.graphMA.get_node_count(), 1)

        self.assertEqual(self.graphMI.get_node_count(), 0)
        self.graphMI.add_node("A", 1.0)
        self.assertEqual(self.graphMI.get_node_count(), 1)

    def test_is_connected(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphLA.is_connected())

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMA.is_connected())

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMI.is_connected())

    def test_is_complete(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.graphLA.add_edge("B", "A", 3.0, "edge2")
        self.assertTrue(self.graphLA.is_complete())

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.graphMA.add_edge("B", "A", 3.0, "edge2")
        self.assertTrue(self.graphMA.is_complete())

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.graphMI.add_edge("B", "A", 3.0, "edge2")
        self.assertTrue(self.graphMI.is_complete())

    def test_is_simple(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphLA.is_simple())

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMA.is_simple())

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMI.is_simple())

    def test_get_bridge(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphLA.get_bridge(), ["edge1"])

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphMA.get_bridge(), ["edge1"])

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphMI.get_bridge(), ["edge1"])

    def test_get_articulations(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_node("C", 3.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.graphLA.add_edge("B", "C", 3.0, "edge2")
        self.assertEqual(self.graphLA.get_articulations(), ["B"])

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_node("C", 3.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.graphMA.add_edge("B", "C", 3.0, "edge2")
        self.assertEqual(self.graphMA.get_articulations(), ["B"])

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_node("C", 3.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.graphMI.add_edge("B", "C", 3.0, "edge2")
        self.assertEqual(self.graphMI.get_articulations(), ["B"])

    def test_thers_node_adjacency(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphLA.thers_node_adjacency("A", "B"))
        self.assertFalse(self.graphLA.thers_node_adjacency("B", "A"))

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMA.thers_node_adjacency("A", "B"))
        self.assertFalse(self.graphMA.thers_node_adjacency("B", "A"))

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMI.thers_node_adjacente("A", "B"))
        self.assertFalse(self.graphMI.thers_node_adjacente("B", "A"))

    def test_thers_edge_by_name(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphLA.thers_edge_by_name("edge1"))
        self.assertFalse(self.graphLA.thers_edge_by_name("edge2"))

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMA.thers_edge_by_name("edge1"))
        self.assertFalse(self.graphMA.thers_edge_by_name("edge2"))

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.assertTrue(self.graphMI.thers_edge_by_name("edge1"))
        self.assertFalse(self.graphMI.thers_edge_by_name("edge2"))

    def test_print_revert_graph(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.graphLA.print_revert_graph()

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.graphMA.print_revert_graph()

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        self.graphMI.print_revert_graph()

    def test_get_all_nodes_degree(self):
        self.graphLA.add_node("A", 1.0)
        self.graphLA.add_node("B", 2.0)
        self.graphLA.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphLA.get_all_nodes_degree(), {"A": 1, "B": 0})

        self.graphMA.add_node("A", 1.0)
        self.graphMA.add_node("B", 2.0)
        self.graphMA.add_edge("A", "B", 3.0, "edge1")
        self.assertEqual(self.graphMA.get_all_nodes_degree(), {"A": 1, "B": 0})

        self.graphMI.add_node("A", 1.0)
        self.graphMI.add_node("B", 2.0)
        self.graphMI.add_edge("A", "B", 3.0, "edge1")
        # self.assertEqual(
        #     self.graphMI.get_all_nodes_degree(), {"A": 1, "B": 0}
        # )  # TODO: Check this implementation, probably is wrong

    def test_kosaraju(self):

        self.graphMA.add_edge(1, 2, 1)
        self.graphMA.add_edge(2, 5, 1)
        self.graphMA.add_edge(5, 3, 1)
        self.graphMA.add_edge(3, 1, 1)

        self.graphMA.add_edge(1, 4, 1)
        self.graphMA.add_edge(4, 6, 1)
        self.graphMA.add_edge(3, 6, 1)

        self.graphMA.add_edge(5, 7, 1)
        self.graphMA.add_edge(6, 7, 1)
        self.graphMA.add_edge(7, 6, 1)
        self.graphMA.to_xml()

        self.graphMI.to_graph("output/graphMA.gexf")
        self.graphLA.to_graph("output/graphMA.gexf")

        self.assertEqual(self.graphMA.kosaraju(), self.graphMI.kosaraju())
        self.assertEqual(self.graphMA.kosaraju(), self.graphLA.kosaraju())

    def test_connectivity_degree(self):
        self.graphMA.add_edge(1, 2, 1)
        self.graphMA.add_edge(2, 5, 1)
        self.graphMA.add_edge(5, 3, 1)
        self.graphMA.add_edge(3, 1, 1)

        self.graphMA.add_edge(1, 4, 1)
        self.graphMA.add_edge(4, 6, 1)
        self.graphMA.add_edge(3, 6, 1)

        self.graphMA.add_edge(5, 7, 1)
        self.graphMA.add_edge(6, 7, 1)
        self.graphMA.add_edge(7, 6, 1)
        self.graphMA.to_xml()

        self.graphMI.to_graph("output/graphMA.gexf")
        self.graphLA.to_graph("output/graphMA.gexf")

        self.assertEqual(
            self.graphMA.connectivity_degree(), self.graphLA.connectivity_degree()
        )
        self.assertEqual(
            self.graphMA.connectivity_degree(), self.graphMI.connectivity_degree()
        )


if __name__ == "__main__":
    unittest.main()
