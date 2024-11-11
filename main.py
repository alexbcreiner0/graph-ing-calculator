from os import remove
from numpy import random as r
from dash import Dash, html, dcc, callback, Input, Output, ctx
import dash_cytoscape as cyto
import plotly.express as px
from dash.exceptions import PreventUpdate
from graph_examples import *
from graph_generators import *

app = Dash(__name__, title= 'Visual Graphing Calculator')

class Graph:
    def __init__(self, adj_list= {}, weighted = False, digraph= True, layout= 'cose'):
        self.is_directed = digraph
        self.is_weighted = weighted
        if not weighted:
            for vertex in adj_list:
                if type(adj_list[vertex]) == dict: # look at the type of the first key
                    self.is_weighted = True
                break
        self.identifier = 'graph'
        self.layout = { 'name': 'cose', 'nodeRepulsion': 400000000, 'idealEdgeLength': 100, 'nodeOverlap': 200, 'edgeElasticity': 0.45, 'padding': 30 }
        self.style = {'width': '100%', 'height': '1000px', 'background-color': '#161A1D'}
        self.stylesheet = [{'selector': 'node', 'style': {'label': 'data(label)', 'color': '#FFFFFF', 'width': '30px', 'height': '30px'}},
			{'selector': '.back', 'style': {'line-color': 'red', 'target-arrow-color': 'red'}},
			{'selector': '.forward', 'style': {'line-color': 'blue', 'target-arrow-color': 'blue'}},
			{'selector': '.cross', 'style': {'line-color': 'green', 'target-arrow-color': 'green'}}]
        if self.is_directed:                                                            
            style = {'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'label': 'data(label)', 'color': '#FFFFFF'}
        else:
            style = {'curve-style': 'bezier', 'label': 'data(label)'}
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

    def get_cytograph(self):
        return cyto.Cytoscape(
            id= self.identifier, 
            layout= self.layout,
            style= self.style, 
            elements= self.elements,
            stylesheet= self.stylesheet,
            wheelSensitivity=0.1
        )

G: Graph = Graph(G_unknown)
# G: Graph = Graph(digraph= True, weighted= True)

def add_edge_to_graph(adj_list, edge, is_directed, is_weighted, weight= ''):
    source = edge[0]
    dest = edge[1]
    if source not in adj_list:
        if is_weighted:
            adj_list[source] = {dest: float(weight)}
        else:
            adj_list[source] = [dest]
    else:
        if is_weighted:
            adj_list[source][dest] = float(weight) if weight != '' else 0.0
        else:
            adj_list[source].append(float(weight)) if weight != '' else 0.0
    print(adj_list)
    return Graph(adj_list, digraph= is_directed, weighted= is_weighted)

def remove_edge_from_graph(adj_list, edge, is_directed, is_weighted):
    source, dest = edge[0], edge[1]
    print(f"Removing the edge {edge}")
    for vertex in adj_list:
        if dest in adj_list[vertex]:
            del adj_list[vertex][dest]
            if not is_directed:
                del adj_list[dest][vertex]
            break
    return Graph(adj_list, digraph= is_directed, weighted= is_weighted)

def add_vertex_to_graph(adj_list, vertex, is_directed, is_weighted):
    if vertex in adj_list:
        return Graph(adj_list, digraph= is_directed, weighted= is_weighted)
    else:
        adj_list[vertex] = {} if is_weighted else []
    return Graph(adj_list, digraph= is_directed, weighted= is_weighted)

def remove_vertex_from_graph(adj_list, vertex, is_directed, is_weighted):
    if vertex not in adj_list:
        return Graph(adj_list, digraph= is_directed, weighted= is_weighted)
    else:
        for node in adj_list:
            if vertex in adj_list[node]:
                if is_weighted: del adj_list[node][vertex]
                else: del adj_list[node][adj_list.index(vertex)]
        del adj_list[vertex]
        return Graph(adj_list, digraph= is_directed, weighted= is_weighted)

@callback(Output(component_id='graph', component_property='layout', allow_duplicate=True), 
	Input('layout dropdown', 'value'), 
	prevent_initial_call='initial_duplicate')
def update_layout(layout):
    if ctx.triggered_id == None:
        raise PreventUpdate
    elif layout == 'cose':
        return { 'name': layout, 'nodeRepulsion': 400000000, 
                'idealEdgeLength': 100, 'nodeOverlap': 200, 
                'edgeElasticity': 0.45, 'padding': 30, 'animate': True,
                'animationEasing': 'ease-in-out', 'animationDuration': 1000000, 'animationThreshold': 0 }
    elif layout == 'concentric':
        return {'name': layout, 'minNodeSpacing': 100, 'equidistant': True, 'padding': 30, 'animate': True}
    return {'name': layout, 'animate': True}

@callback(Output(component_id='graph', component_property='elements'),
          Input(component_id='add_edge', component_property='n_clicks'),
          Input(component_id='new_edge_source_field', component_property='value'),
          Input(component_id='new_edge_dest_field', component_property='value'),
          Input(component_id='new_edge_weight_field', component_property='value'),
          Input(component_id='remove_edge', component_property='n_clicks'),
          Input(component_id='add_vertex', component_property='n_clicks'),
          Input(component_id='remove_vertex', component_property='n_clicks'),
          Input(component_id='vertex_name', component_property='value'))
def add_new_edge(add_edge, new_edge_source_field, new_edge_dest_field, new_edge_weight_field, remove_edge, add_vertex, remove_vertex, vertex_name):
    # print(ctx.triggered_id)
    global G
    if ctx.triggered_id in [None, 'new_edge_source_field', 'new_edge_dest_field', 'new_edge_weight_field', 'vertex_name']: raise PreventUpdate
    elif ctx.triggered_id == 'add_edge':
        G = add_edge_to_graph(
            G.adj_list, 
            (new_edge_source_field, new_edge_dest_field),
            G.is_directed,
            G.is_weighted,
            new_edge_weight_field
        )
        return G.elements
    elif ctx.triggered_id == 'remove_edge':
        G = remove_edge_from_graph(
            G.adj_list,
            (new_edge_source_field, new_edge_dest_field),
            G.is_directed,
            G.is_weighted,
        )
        return G.elements
    elif ctx.triggered_id == 'add_vertex':
        G = add_vertex_to_graph(
            G.adj_list,
            vertex_name,
            G.is_directed,
            G.is_weighted
        )
        return G.elements
    elif ctx.triggered_id == 'remove_vertex':
        G = remove_vertex_from_graph(
            G.adj_list,
            vertex_name,
            G.is_directed,
            G.is_weighted
        )
        return G.elements

def get_dropdown_row():
    options_list = [
        {'label': 'Grid', 'value': 'grid'}, 
        {'label': 'Random', 'value': 'random'},
        {'label': 'Circle', 'value': 'circle'}, 
        {'label': 'Cose', 'value': 'cose'}, 
        {'label': 'Concentric', 'value': 'concentric'}
    ]
    dropdown_row = html.Div(
        [
            html.H3(
                'Display Style: ',
                style = {'margin-right': '10px'}
            ),
            dcc.Dropdown(
                id='layout dropdown', 
                value='circle', 
                clearable=False, 
                options=options_list,
                style={'flex-grow': '1'}
            )
        ],
        style= {'display': 'flex', 'flex_direction': 'row', 'align-items': 'center'}
    )
    return dropdown_row


def get_graph_edit_row():
    return html.Div(
        [
            # Section for edge controls
            html.Div(
                [
                    html.H3('Add/remove an edge', style={'margin-right': '10px'}),
                    html.Div(
                        [
                            html.Label('Source name:', style={'margin-right': '5px'}),
                            dcc.Input(
                                id='new_edge_source_field', 
                                value='', 
                                type='text',
                                style={'width': '80px', 'margin-right': '10px'}
                            ),
                            html.Label('Dest name:', style={'margin-right': '5px'}),
                            dcc.Input(
                                id='new_edge_dest_field',
                                value='',
                                type='text',
                                style={'width': '80px', 'margin-right': '10px'}
                            ),
                            html.Label('Weight:', style={'margin-right': '5px'}),
                            dcc.Input(
                                id='new_edge_weight_field',
                                value='',
                                type='text',
                                style={'width': '80px', 'margin-right': '10px'}
                            ),
                            html.Button('Add', id='add_edge', style={'margin-right': '5px'}),
                            html.Button('Remove', id='remove_edge')
                        ],
                        style={'display': 'flex', 'align-items': 'center'}
                    ),
                ],
                style={'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px', 'margin-right': '20px'}
            ),
            
            # Section for vertex controls
            html.Div(
                [
                    html.H3('Add/remove a vertex', style={'margin-right': '10px'}),
                    html.Div(
                        [
                            html.Label('Vertex name:', style={'margin-right': '5px'}),
                            dcc.Input(
                                id='vertex_name',
                                value='',
                                type='text',
                                style={'width': '80px', 'margin-right': '10px'}
                            ),
                            html.Button('Add', id='add_vertex', style={'margin-right': '5px'}),
                            html.Button('Remove', id='remove_vertex')
                        ],
                        style={'display': 'flex', 'align-items': 'center'}
                    ),
                ],
                style={'padding': '10px', 'border': '1px solid #ccc', 'border-radius': '5px'}
            )
        ],
        style={'display': 'flex', 'align-items': 'center'}
    )

# def get_graph_edit_row():
#     return html.Div(
#         [
#             html.H3(
#                 'Add/remove an edge',
#                 style = {'margin-right': '10px'}
#             ),
#             html.H3(
#                 'Source name: ',
#                 style = {'margin-right': '10px'}
#             ),
#             dcc.Input(
#                 id= 'new_edge_source_field', 
#                 value= '', 
#                 type= 'text',
#                 style= {'min-width': '30px', 'min-height': '30px'}
#             ),
#             html.H3(
#                 'Dest name: ',
#                 style = {'margin-right': '10px'}
#             ),
#             dcc.Input(
#                 id= 'new_edge_dest_field',
#                 value= '',
#                 type= 'text',
#                 style= {'min-width': '30px', 'min-height': '30px'}
#             ),
#             html.H3(
#                 'Weight (if applicable): ',
#                 style = {'margin-right': '10px'}
#             ),
#             dcc.Input(
#                 id= 'new_edge_weight_field',
#                 value= '',
#                 type= 'text',
#                     style= {'min-width': '30px', 'min-height': '30px'}
#             ),
#             html.Button(
#                 'Add',
#                 id= 'add_edge',
#                 style= {'min-height': '30px'}
#             ),
#             html.Button(
#                 'Remove',
#                 id= 'remove_edge',
#                 style= {'min-height': '30px'}
#             ),
#             html.H3(
#                 "Add/remove a vertex",
#                 style = {'margin-right': '10px'}
#             ),
#             html.H3(
#                 "Vertex name",
#                 style = {'margin-right': '10px'}
#             ),
#             dcc.Input(
#                 id= 'vertex_name',
#                 value= '',
#                 type= 'text',
#                 style= {'min-width': '30px', 'min-height': '30px'}
#             ),
#             html.Button(
#                 'Add',
#                 id= 'add_vertex',
#                 style= {'min-height': '30px'}
#             ),
#             html.Button(
#                 'Remove',
#                 id= 'remove_vertex',
#                 style= {'min-height': '30px'}
#             )
#         ],
#         style= { 'display': 'flex', 'flex_direction': 'row', 'align-items': 'center' }
#     )

if __name__ == '__main__':
    cyto.load_extra_layouts()
    # extra_edges = False

    graph_display = html.Div(G.get_cytograph())
    dropdown_row = get_dropdown_row()
    add_elements_row = get_graph_edit_row()
    title = html.H1("'Graphing' Calculator")
    # remove_elements_row = get_graph_remove_row()

    display_panel = html.Div(
        children= [ graph_display ],
        style={'flex': '2', 'padding': '10px'}
    )

    control_panel = html.Div(
        children= [ title, dropdown_row, add_elements_row ],
        style={'flex': '1', 'padding': '10px'}
    )

    app.layout = html.Div(
        children= [control_panel, display_panel],
        style= { 'display': 'flex', 'flex-direction': 'row', 'gap': '20px', 'min-height': '100vh' }
    )

    app.run(debug= True)
    
