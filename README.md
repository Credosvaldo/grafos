# Graph Library

This library provides implementations for three types of graph representations: Adjacency List, Incidence Matrix, and Adjacency Matrix. Each representation is encapsulated in its respective class: `GrafoLA`, `GrafoMI`, and `GrafoMA`.

## Classes

### GrafoLA (Adjacency List)
The `GrafoLA` class represents a graph using an adjacency list. This is efficient for sparse graphs.

#### Key Methods:
- `add_node(name: str, weight: float = 1.0)`: Adds a new node to the graph.
- `remove_node(name: str)`: Removes a node and its associated edges from the graph.
- `add_edge(predecessor: str, successor: str, weight: float = 1, name: str = None)`: Adds an edge to the graph.
- `remove_edge_by_name(name: str)`: Removes an edge from the graph by its name.
- `is_connected()`: Checks if the graph is connected.
- `get_euler_path(by_tarjan: bool = True)`: Gets the Euler path of the graph.

### GrafoMI (Incidence Matrix)
The `GrafoMI` class represents a graph using an incidence matrix. This is useful for certain types of graph algorithms.

#### Key Methods:
- `add_node(name: str, weight: float = 1.0)`: Adds a new node to the graph.
- `remove_node(name: str)`: Removes a node and its associated edges from the graph.
- `add_edge(predecessor: str, successor: str, weight: float = 1, name: str = None)`: Adds an edge to the graph.
- `remove_edge_by_name(name: str)`: Removes an edge from the graph by its name.
- `is_connected()`: Checks if the graph is connected.
- `get_euler_path(by_tarjan: bool = True)`: Gets the Euler path of the graph.

### GrafoMA (Adjacency Matrix)
The `GrafoMA` class represents a graph using an adjacency matrix. This is efficient for dense graphs.

#### Key Methods:
- `add_node(name: str, weight: float = 1.0)`: Adds a new node to the graph.
- `remove_node(name: str)`: Removes a node and its associated edges from the graph.
- `add_edge(predecessor: str, successor: str, weight: float = 1, name: str = None)`: Adds an edge to the graph.
- `remove_edge_by_name(name: str)`: Removes an edge from the graph by its name.
- `is_connected()`: Checks if the graph is connected.
- `get_euler_path(by_tarjan: bool = True)`: Gets the Euler path of the graph.

## Installation
To use this library, simply clone the repository and import the desired graph class into your project.

```bash
git clone https://github.com/yourusername/graph-library.git
```

## Usage
Here is an example of how to use the `GrafoLA` class:

```python
from GrafoLA import GrafoLA

# Create a new graph
graph = GrafoLA(DIRECTED=True, num_nodes=3, nodes=[("A", 1.0), ("B", 1.0), ("C", 1.0)])

# Add edges
graph.add_edge("A", "B", weight=2.0)
graph.add_edge("B", "C", weight=3.0)

# Check if the graph is connected
print(graph.is_connected())

# Get the Euler path
print(graph.get_euler_path())
```

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Authors
- Pedro Henrique Pires Rodrigues  
- Pedro Negri Leão Lambert
- Vinicius Rezende Arantes de Araujo Moreira
For more details, refer to the individual class files: [GrafoLA.py](#file:GrafoLA.py-context), [GrafoMI.py](#file:GrafoMI.py-context), and [GrafoMA.py](#file:GrafoMA.py-context).