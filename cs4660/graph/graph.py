"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that graph object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """

    f = open(file_path)     #opens file from file_path
    firstLine = True        #setting firstLine true to use first line only

    if isinstance(graph, AdjacencyList):
        for line in f:
            if firstLine:
                nodeTot = int(line)
                for x in range(0, nodeTot):
                    AdjacencyList.add_node(graph, Node(x))
                firstLine = False
            else:
                edgeSplit = []
                edgeSplit = line.strip().split(":")
                edge = Edge(Node(int(edgeSplit[0])), Node(int(edgeSplit[1])), int(edgeSplit[2]))
                AdjacencyList.add_edge(graph, edge)

    if isinstance(graph, AdjacencyMatrix):
        for line in f:
            if firstLine:
                nodeTot = int(line)
                graph.adjacency_matrix = [[0 for x in range(nodeTot)] for y in range(nodeTot)]
                for x in range(0, nodeTot):
                    AdjacencyMatrix.add_node(graph, Node(x))
                firstLine = False
            else:
                edgeSplit = []
                edgeSplit = line.strip().split(":")
                edge = Edge(Node(int(edgeSplit[0])), Node(int(edgeSplit[1])), int(edgeSplit[2]))
                AdjacencyMatrix.add_edge(graph, edge)

    if isinstance(graph, ObjectOriented):
        for line in f:
            if firstLine:
                nodeTot = int(line)
                for x in range(0, nodeTot):
                    ObjectOriented.add_node(graph, Node(x))
                firstLine = False
            else:
                pass
                edgeSplit = []
                edgeSplit = line.strip().split(":")
                edge = Edge(Node(int(edgeSplit[0])), Node(int(edgeSplit[1])), int(edgeSplit[2]))
                ObjectOriented.add_edge(graph, edge)

    f.close
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight


    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))

class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        node_1_values = self.adjacency_list.get(node_1)

        for i in node_1_values:
            if i.to_node == node_2:
                return True
        return False


    def neighbors(self, node):
        node_values = self.adjacency_list.get(node)
        neighbor = []
        for i in node_values:
            neighbor.append(i.to_node)

        return neighbor

    def add_node(self, node):
        if node in self.adjacency_list:
            return False
        else:
            self.adjacency_list[node] = []
            return True

    def remove_node(self, node):
        if node in self.adjacency_list.keys():
            self.adjacency_list.pop(node)
            for i in self.adjacency_list.values():
                for j in i:
                    if j.to_node == node:
                        resetNode = j.from_node
                        resetValues = self.adjacency_list[resetNode]
                        self.adjacency_list[resetNode] = []
                        for x in resetValues:
                            if node != x.to_node:
                                self.adjacency_list[resetNode].append(x)
            return True
        return False

    def add_edge(self, edge):
        if edge in self.adjacency_list[edge.from_node]:
            return False
        else:
            self.adjacency_list[edge.from_node].append(edge)
            return True

    def remove_edge(self, edge):
        if edge in self.adjacency_list[edge.from_node]:
            for i in self.adjacency_list.values():
                for j in i:
                    if j.from_node == edge.from_node and j.to_node == edge.to_node:
                        resetNode = j.from_node
                        resetValues = self.adjacency_list[resetNode]
                        self.adjacency_list[resetNode] = []
                        for x in resetValues:
                            if edge != x:
                                self.adjacency_list[resetNode].append(x)
                        return True
        return False

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        x = self.__get_node_index(node_1)
        y = self.__get_node_index(node_2)
        if self.adjacency_matrix[x][y] != 0:
            return True
        return False

    def neighbors(self, node):
        x = self.__get_node_index(node)
        neighbor = []
        for count, i in enumerate(self.adjacency_matrix[x][:]):
            if i != 0:
                neighbor.append(Node(count))
        return neighbor


    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node)
            return True

    def remove_node(self, node):
        if node in self.nodes:
            temp = [[0 for x in range(len(self.nodes)-1)] for y in range(len(self.nodes)-1)]
            rowcount = 0
            for counti, i in enumerate(self.adjacency_matrix):
                if counti != self.__get_node_index(node):
                    columncount = 0
                    for countj, j in enumerate(i):
                        if countj != self.__get_node_index(node):
                            temp[rowcount][columncount] = j
                            columncount += 1
                    rowcount += 1
            self.adjacency_matrix = temp
            self.nodes.remove(node)
            return True
        return False

    def add_edge(self, edge):
        x = self.__get_node_index(edge.from_node)
        y = self.__get_node_index(edge.to_node)
        if self.adjacency_matrix[x][y] == 0:
            self.adjacency_matrix[x][y] = edge.weight
            return True
        return False

    def remove_edge(self, edge):
        xindex = self.__get_node_index(edge.from_node)
        yindex = self.__get_node_index(edge.to_node)
        e_weight = edge.weight

        if self.adjacency_matrix[xindex][yindex] != 0:
            self.adjacency_matrix[xindex][yindex] = 0
            return True
        return False

    def __get_node_index(self, node):
        """helper method to find node index"""
        return self.nodes.index(node)

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for i in self.edges:
            if i.from_node == node_1:
                if i.to_node == node_2:
                    return True
        return False

    def neighbors(self, node):
        neighbor = []
        for i in self.edges:
            if i.from_node == node:
                neighbor.append(i.to_node)
        return neighbor

    def add_node(self, node):
        if node in self.nodes:
            return False
        self.nodes.append(node)
        return True

    def remove_node(self, node):
        if node in self.nodes:
            for i in self.edges:
                if i.to_node == node:
                    self.edges.remove(i)
            self.nodes.remove(node)
            return True
        return False

    def add_edge(self, edge):
        if edge in self.edges:
            return False
        self.edges.append(edge)
        return True

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        return False

