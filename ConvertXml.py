from GrafoMA import GrafoMA
from GrafoLA import GrafoLA
from GraphType import GraphType
import xmltodict

from NodeLA import NodeLA


class ConvertXml:
    def __init__(self):
        self.xml = {}

    def toDict(self):
        return self.xml

    def toXml(self, graphType: GraphType, graph):
        if graphType == GraphType.LIST_ADJACENCY:
            self.__basedInListAdjacency(graph)
        elif graphType == GraphType.MATRIX_INCIDENCE:
            self.__basedInMatrixIncidence(graph)
        elif graphType == GraphType.MATRIX_ADJACENCY:
            self.__basedInMatrixAdjacency(graph)
        else:
            raise ValueError("Invalid GraphType")
        return self.xml

    def __basedInListAdjacency(self, graph):
        pass

    def __basedInMatrixIncidence(self, graph):
        pass

    def __basedInMatrixAdjacency(self, graph):
        pass

    def to_graph(self, graphType: GraphType, path: str):

        with open(path, "rb") as file:
            self.xml = xmltodict.parse(file)

        nodes = self.xml["gexf"]["graph"]["nodes"]["node"]
        edges = self.xml["gexf"]["graph"]["edges"]["edge"]
        directed = self.xml["gexf"]["graph"]["@defaultedgetype"] == "directed"

        if graphType == GraphType.LIST_ADJACENCY:
            graph = GrafoMA(DIRECTED=directed)
        elif graphType == GraphType.MATRIX_INCIDENCE:
            pass
        elif graphType == GraphType.MATRIX_ADJACENCY:
            graph = GrafoLA(DIRECTED=directed)
        else:
            raise ValueError("Invalid GraphType")

        for node in nodes:
            graph.add_node(node["@label"], node["attvalues"]["attvalue"]["@value"])

        if edges == None:
            return graph
        print(len(edges))
        if len(edges) == 4 and edges["@source"] != None:
            edges = [edges]

        for edge in edges:
            for node in nodes:
                if (edge["@source"]) == node["@id"]:
                    source = node["@label"]
                if edge["@target"] == node["@id"]:
                    target = node["@label"]

            graph.add_edge(source, target, edge["@weight"], edge["@label"])
        return graph

    
