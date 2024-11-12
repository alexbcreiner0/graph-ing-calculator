import dash_cytoscape as cyto
from settings import LAYOUT_SETTINGS

class Graph:
    def __init__(self, adj_list= {}, weighted = False, digraph= True, layout= 'grid'):
        self.is_directed = digraph
        self.is_weighted = weighted
        if not weighted:
            for vertex in adj_list:
                if type(adj_list[vertex]) == dict: # look at the type of the first key
                    self.is_weighted = True
                break
        self.identifier = 'graph'
        self.layout = LAYOUT_SETTINGS[layout]
        self.style = {'width': '100%', 'height': '1000px', 'background-color': '#161A1D'}
        self.stylesheet = [{'selector': 'node', 'style': {'label': 'data(label)', 'color': '#FFFFFF', 'width': '30px', 'height': '30px'}},
			{'selector': '.back', 'style': {'line-color': 'red', 'target-arrow-color': 'red'}},
			{'selector': '.forward', 'style': {'line-color': 'blue', 'target-arrow-color': 'blue'}},
			{'selector': '.cross', 'style': {'line-color': 'green', 'target-arrow-color': 'green'}}]
        if self.is_directed:                                                            
            style = {'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'label': 'data(label)', 'color': '#FFFFFF'}
        else:
            style = {'curve-style': 'bezier', 'label': 'data(label)' }
        self.stylesheet.append({'selector': 'edge', 'style': style})

        self.adj_list = adj_list
        self.__patch_list(self.is_weighted) # add keys for isolated vertices
        
        # create lists of vertices and edges
        self.vertices = list(adj_list.keys())
        self.edges, self.weights = self.__prepare_edge_list()
        
        # At this point, should have complete lists of vertices and edges, and a complete dictionary of weights if applicable. 
        # If the graph is undirected, then the adjacency list itself needs to potentially be added to
        self.__update_adj_list()

        # create elements list for cytoscape, and directories for id values of edges and vertices
        self.elements, self.vertex_directory, self.edge_directory = self.__create_elements()

    def __patch_list(self, weighted):
        '''Helper method for the constructor, ensuring that every vertex is a key in the adj list'''
        value_lists =list(self.adj_list.values())
        union = set()
        for l in value_lists:
            union |= set(l)
        if not weighted:
            new_keys = {vertex: [] for vertex in union if vertex not in self.adj_list.keys()}
            self.adj_list.update(new_keys)
        else:
            new_keys = {vertex: {} for vertex in union if vertex not in self.adj_list.keys()}
            self.adj_list.update(new_keys)
        
    def __prepare_edge_list(self):
        edges = []
        weights = {}
        for vertex, neighbors in self.adj_list.items():
            for neighbor in neighbors:
                edges.append((vertex, neighbor))
                if self.is_weighted:
                    weights[(vertex, neighbor)] = self.adj_list[vertex][neighbor]
                if not self.is_directed:
                    edges.append((neighbor, vertex))
                    if self.is_weighted:
                        weights[(neighbor, vertex)] = self.adj_list[vertex][neighbor]
        return list(set(edges)), weights # remove any redundant edges

    def __update_adj_list(self):
        for edge in self.edges:
            if edge[1] not in self.adj_list[edge[0]]:
                if self.is_weighted:
                    self.adj_list[edge[0]][edge[1]] = self.weights[edge]
                else:
                    self.adj_list[edge[0]].append(edge[1])

    def __create_elements(self):
        vertex_directory = {}
        edge_directory = {}
        elements = []
        counter = 0
        for vertex in self.vertices:
            vertex_data = {'id': str(vertex), 'label': str(vertex)}
            node = {'data': vertex_data, 'grabbable': True, 'selectable': True}
            elements.append(node)
            vertex_directory[str(vertex)] = counter
            counter += 1
        for edge in self.edges:
            if not self.is_directed and str(edge[1])+str(edge[0]) in edge_directory:
                continue
            edge_data = {
                'id': str(edge[0])+str(edge[1]),
                'source': str(edge[0]),
                'target': str(edge[1]),
                'label': str(self.weights[edge]) if self.is_weighted and edge in self.weights else ''
            }
            elements.append({'data': edge_data})
            edge_directory[str(edge[0])+str(edge[1])] = counter
            counter += 1
        return elements, vertex_directory, edge_directory

    def __str__(self):
        return str(self.adj_list)

    def to_dict(self):
        output = vars(self)
        if "weights" in output: del output["weights"]
        if "edges" in output: del output["edges"]
        return output

    def get_cytograph(self):
        return cyto.Cytoscape(
            id= self.identifier, 
            layout= self.layout,
            style= self.style, 
            elements= self.elements,
            stylesheet= self.stylesheet,
            wheelSensitivity=0.1
        )

