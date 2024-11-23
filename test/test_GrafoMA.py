import unittest
from GrafoMA import GrafoMA


class TestGrafoMA(unittest.TestCase):

    def setUp(self):
        self.graph = GrafoMA(
            DIRECTED=True, num_nodes=3, nodes=[("A", 1.0), ("B", 2.0), ("C", 3.0)]
        )

    def test_add_node(self):
        self.graph.add_node("D", 4.0)
        self.assertEqual(self.graph.get_node_count(), 4)
        self.assertIn("D", self.graph.nodes_map)
        self.assertEqual(self.graph.nodes_map["D"].weight, 4.0)

    def test_add_edge(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.assertEqual(self.graph.get_edge_count(), 1)
        self.assertIn("edge1", self.graph.edges_map)
        self.assertEqual(self.graph.edges_map["edge1"], ("A", "B", 0))

    def test_remove_edge_by_name(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.graph.remove_edge_by_name("edge1")
        self.assertEqual(self.graph.get_edge_count(), 0)
        self.assertNotIn("edge1", self.graph.edges_map)

    def test_remove_all_edge_by_nodes(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.graph.add_edge("A", "B", 2.0, "edge2")
        self.graph.remove_all_edge_by_nodes("A", "B")
        self.assertEqual(self.graph.get_edge_count(), 0)

    def test_remove_node(self):
        self.graph.add_node("D", 4.0)
        self.graph.remove_node("D")
        self.assertEqual(self.graph.get_node_count(), 3)
        self.assertNotIn("D", self.graph.nodes_map)

    def test_is_connected(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.graph.add_edge("B", "C", 1.0, "edge2")
        self.assertTrue(self.graph.is_connected())

    def test_is_not_connected(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.assertFalse(self.graph.is_connected())

    def test_get_bridge(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.graph.add_edge("B", "C", 1.0, "edge2")
        self.assertEqual(self.graph.get_bridge(), ["edge1", "edge2"])

    def test_get_articulations(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.graph.add_edge("B", "C", 1.0, "edge2")
        self.assertEqual(self.graph.get_articulations(), ["B"])

    def test_get_euler_path(self):
        graph = GrafoMA(
            DIRECTED=False, num_nodes=3, nodes=[("A", 1.0), ("B", 2.0), ("C", 3.0)]
        )
        graph.add_edge("A", "B", 1.0, "edge1")
        graph.add_edge("B", "C", 1.0, "edge2")
        graph.add_edge("C", "A", 1.0, "edge3")
        self.assertEqual(graph.get_euler_path(), ["A", "B", "C"])

    def test_to_xml(self):
        self.graph.add_edge("A", "B", 1.0, "edge1")
        self.graph.to_xml()
        with open("output/graphMA.gexf", "r") as file:
            content = file.read()
        self.assertIn('<node id="A" label="A">', content)
        self.assertIn(
            "<edge label='edge1' source='A' target='B' weight='1.0'/>", content
        )

    def test_to_graph(self):
        aux = GrafoMA(
            DIRECTED=False, num_nodes=3, nodes=[("A", 1.0), ("B", 2.0), ("C", 3.0)]
        )
        aux.to_xml()
        new_graph = GrafoMA()
        new_graph.to_graph("output/graphMA.gexf")
        self.assertEqual(new_graph.get_node_count(), 3)
        self.assertEqual(new_graph.get_edge_count(), 0)

    def test_is_empty(self):
        self.assertTrue(self.graph.is_empty())
        self.graph.add_node("F")
        self.assertFalse(self.graph.is_empty())

    def test_is_complete(self):
        self.graph.add_node("F")
        self.graph.add_node("AS")
        self.graph.add_edge("F", "AS")
        self.assertFalse(self.graph.is_complete())
        self.graph.add_edge("AS", "A")
        self.assertTrue(self.graph.is_complete())

    def test_is_simple(self):
        self.graph.add_node("F")
        self.graph.add_node("AS")
        self.graph.add_edge("F", "AS")
        self.assertTrue(self.graph.is_simple())
        self.graph.add_edge("F", "AS", name="edge2")
        self.assertFalse(self.graph.is_simple())

    def test_get_all_nodes_degree(self):
        self.graph.add_node("F")
        self.graph.add_node("AS")
        self.graph.add_edge("F", "AS")
        degrees = self.graph.get_all_nodes_degree()
        self.assertEqual(degrees["A"], 1)
        self.assertEqual(degrees["AS"], 1)

    def test_get_edges_by_node(self):
        self.graph.add_node("F")
        self.graph.add_node("AS")
        self.graph.add_edge("F", "AS", name="edge1")
        edges = self.graph.get_edges_by_node("F")
        self.assertEqual(edges, ["edge1"])

    def test_is_bridge(self):
        self.graph.add_node("F")
        self.graph.add_node("AS")
        self.graph.add_edge("F", "AS", name="edge1")
        self.assertTrue(self.graph.is_bridget("edge1"))

    def test_get_euler_path(self):
        self.graph = GrafoMA(DIRECTED=False)
        self.graph.add_node("F")
        self.graph.add_node("AS")
        self.graph.add_node("C")
        self.graph.add_edge("F", "AS")
        self.graph.add_edge("AS", "C")
        self.graph.add_edge("C", "A")
        self.assertEqual(self.graph.get_euler_path(), ["F", "AS", "C"])


if __name__ == "__main__":
    unittest.main()
