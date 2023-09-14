class Tree:
    def __init__(self, nodes, edges):
        self._nodes = nodes
        self._edges = edges
    
    def get_nodes(self):
        return self._nodes
    
    def get_edges(self):
        return self._edges
    
    def set_nodes(self, nodes):
        self._nodes = nodes

    def set_edges(self, edges):
        self._edges = edges

    def add_node(self, node):
        self._nodes.append(node)

    def add_edge(self, edge):
        self._edges.append(edge)