# Methods with the same signature in GrafoLA, GrafoMA, and GrafoMI
common_methods = [
    "add_edge(self, predecessor: str, successor: str, weight: float, name: str = None)",
    "remove_edge_by_name(self, name: str)",
    "remove_all_edge_by_nodes(self, predecessor: str, successor: str)",
    "add_node(self, name: str, weight: float = 1.0)",
    "remove_node(self, name: str)",
    "thers_node_adjacency(self, predecessor: str, successor: str)",
    "thers_only_one_edge_btwn_nodes(self, predecessor: str, successor: str)",
    "get_all_nodes_degree(self)",
    "thers_edge_by_name(self, name: str)",
    "thers_edge_by_nodes(self, predecessor: str, successor: str)",
    "thers_edge_adjacency(self, ed1: str, ed2: str)",
    "get_edges_by_node(self, node_name: str)",
    "is_empty(self)",
    "get_edge_count(self)",
    "get_node_count(self)",
    "is_complete(self)",
    "is_simple(self)",
    "is_connected(self)",
    "get_euler_path(self, by_tarjan: bool = True)",
    "make_revert_graph(self)",
    "print_revert_graph(self)",
    "kosaraju(self)",
    "get_bridge(self)",
    "is_bridget(self, edge_name: str)",
    "get_articulations(self)",
    "is_articulation(self, node_name: str)",
    "make_underlying_graph(self)",
    "print_underlying_graph(self)",
    "to_graph(self, path: str)",
    "to_xml(self)",
    "connectivity_degree(self)",
    "reachable(self, v1: str, v2: str, results: Dict[str, Dict[str, DFSNode]])",
    "get_bridge_by_tarjan(self)",
    "is_bridge_by_tarjan(self, edge_name: str)"
]

# Methods with different signatures in GrafoLA, GrafoMA, and GrafoMI
different_methods = {
    "GrafoLA": [
        "create_adjacency_list(self, num_nodes: int, nodes: List[Tuple[str, float]] = [], edges: List[Tuple[str, str, float]] = [])",
        "remove_edge(self, edge_name: str)",
        "get_edge_by_nodes(self, predecessor: str, successor: str)",
        "to_graph(self, path: str)",
        "to_xml(self)",
        "__writeGraph(self)",
        "__writeNode(self, node: NodeLA)",
        "__writeEdge(self, edge: str)",
        "_get_dfs_result_structure(self, nodes_group: List[str] = None)",
        "_tarjan_dfs(self, node_name: str, result: Dict[str, TarjansNode], bridges: List[str], time: List[int])"
    ],
    "GrafoMA": [
        "print_weight_matrix(self)",
        "show_some(self)",
        "remove_all_edge_by_node(self, node_name: str)",
        "is_bridget(self, edge_name: str)",
        "get_edge_by_nodes(self, predecessor: str, successor: str)",
        "to_graph(self, path: str)",
        "to_xml(self)",
        "__writeGraph(self)",
        "__writeNode(self, node_name: str)",
        "__writeEdge(self, edge_name: str)",
        "_get_dfs_result_structure(self, nodes_group: List[str] = None)",
        "_tarjan_dfs(self, node_name: str, result: Dict[str, TarjansNode], bridges: List[str], time: List[int])",
        "_create_random_edges(self)"
    ],
    "GrafoMI": [
        "remove_edge_by_name(self, name: str)",
        "remove_all_edges_by_nodes(self, predecessor: str, sucessor: str)",
        "add_node(self, name: str, weight: float = 1)",
        "remove_node(self, name: str)",
        "thers_node_adjacency(self, predecessor: str, sucessor: str)",
        "thers_only_one_edge_btwn_nodes(self, predecessor: str, sucessor: str)",
        "thers_edge_adjacente(self, edge1: str, edge2: str)",
        "thers_edge_by_name(self, name: str)",
        "thers_edge_by_nodes(self, predecessor: str, sucessor: str)",
        "get_edge_count(self)",
        "get_node_count(self)",
        "is_empty(self)",
        "is_complete(self)",
        "is_simple(self)",
        "connectivity_degree(self)",
        "reachable(self, v1: str, v2: str, results: Dict[str, Dict[str, DFSNode]])",
        "is_connected(self)",
        "get_bridge(self)",
        "is_brige(self, edge_name: str)",
        "get_articulations(self)",
        "is_articulation(self, node_name: str)",
        "make_underlying_graph(self)",
        "print_underlying_graph(self)",
        "to_graph(self, path: str)",
        "to_xml(self)",
        "__writeGraph(self)",
        "__writeNode(self, node_name: str)",
        "__writeEdge(self, edge: str)",
        "kosaraju(self)",
        "_tarjan_dfs(self, node_name: str, result: Dict[str, TarjansNode], bridges: List[str], time: List[int])",
        "get_bridge_by_tarjan(self)",
        "is_bridge_by_tarjan(self, edge_name: str)"
    ]
}






