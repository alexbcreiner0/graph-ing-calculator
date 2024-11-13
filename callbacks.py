from dash import Input, Output, ctx
from random import randint
from dash.exceptions import PreventUpdate
from settings import *
from graph import Graph
from graph_generators import erdos_renyi_random_graph, random_graph

def add_edge_to_graph(adj_list, edge, is_directed, is_weighted, current_layout, weight= ''):
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
    return Graph(adj_list, digraph= is_directed, weighted= is_weighted, layout= current_layout['name'])

def remove_edge_from_graph(adj_list, edge, is_directed, is_weighted):
    source, dest = edge[0], edge[1]
    print(f"Removing the edge {edge}")
    if dest in adj_list[source]:
        if is_weighted:
            del adj_list[source][dest]
        else:
            del adj_list[source][adj_list[source].index(dest)]
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

def register_callbacks(app):
    @app.callback(Output(component_id='graph', component_property='layout', allow_duplicate=True), 
        Input('layout dropdown', 'value'), 
        prevent_initial_call='initial_duplicate')
    def update_layout(layout):
        if ctx.triggered_id == None:
            raise PreventUpdate
        else:
            return LAYOUT_SETTINGS[layout]

    @app.callback(Output(component_id='graph', component_property='elements'),
                  Output(component_id='current_graph', component_property='data'),
                  Output(component_id='graph', component_property='stylesheet'),
                  Output(component_id='layout dropdown', component_property='value'),
                  Input(component_id='current_graph', component_property='data'),
                  Input(component_id='add_edge', component_property='n_clicks'),
                  Input(component_id='new_edge_source_field', component_property='value'),
                  Input(component_id='new_edge_dest_field', component_property='value'),
                  Input(component_id='new_edge_weight_field', component_property='value'),
                  Input(component_id='remove_edge', component_property='n_clicks'),
                  Input(component_id='add_vertex', component_property='n_clicks'),
                  Input(component_id='remove_vertex', component_property='n_clicks'),
                  Input(component_id='vertex_name', component_property='value'),
                  Input(component_id='new_graph_button', component_property='n_clicks'),
                  Input(component_id='num_nodes_field_new_graph', component_property='value'),
                  Input(component_id='num_edges_field_new_graph', component_property='value'),
                  Input(component_id='new_graph_checkboxes', component_property='value'))
    def add_new_edge(current_graph, add_edge, new_edge_source_field, new_edge_dest_field, new_edge_weight_field, remove_edge, add_vertex, remove_vertex, vertex_name, new_graph_button, num_nodes_field_new_graph, num_edges_field_new_graph, new_graph_checkboxes):
        # print(ctx.triggered_id)
        if ctx.triggered_id in [None, 'new_graph_checkboxes', 'current_graph', 'num_edges_field_new_graph', 'num_nodes_field_new_graph', 'new_edge_source_field', 'new_edge_dest_field', 'new_edge_weight_field', 'vertex_name']: raise PreventUpdate
        elif ctx.triggered_id == 'add_edge':
            G = add_edge_to_graph(
                current_graph['adj_list'], 
                (new_edge_source_field, new_edge_dest_field),
                current_graph['is_directed'],
                current_graph['is_weighted'],
                current_graph['layout'],
                new_edge_weight_field
            )
            return G.elements, G.to_dict(), G.stylesheet, current_graph['layout']['name']
        elif ctx.triggered_id == 'remove_edge':
            G = remove_edge_from_graph(
                current_graph['adj_list'],
                (new_edge_source_field, new_edge_dest_field),
                current_graph['is_directed'],
                current_graph['is_weighted'],
            )
            return G.elements, G.to_dict(), G.stylesheet, current_graph['layout']['name']
        elif ctx.triggered_id == 'add_vertex':
            G = add_vertex_to_graph(
                current_graph['adj_list'],
                vertex_name,
                current_graph['is_directed'],
                current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet, current_graph['layout']['name']
        elif ctx.triggered_id == 'remove_vertex':
            G = remove_vertex_from_graph(
                current_graph['adj_list'],
                vertex_name,
                current_graph['is_directed'],
                current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet, current_graph['layout']['name']
        elif ctx.triggered_id == 'new_graph_button':
            random_layout = LAYOUT_LIST[randint(0,4)]
            try:
                num_nodes = int(num_nodes_field_new_graph)
            except ValueError:
                num_nodes = 7
            try:
                num_edges = int(num_edges_field_new_graph)
            except ValueError:
                num_edges = 7
            if 'new_graph_is_directed' in new_graph_checkboxes:
                if 'new_graph_is_weighted' in new_graph_checkboxes and 'new_graph_is_acyclic' in new_graph_checkboxes:
                    G = Graph( # directed, weighted, acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), weighted= True, acyclic= True),
                        weighted= True,
                        digraph= True,
                        layout= random_layout)
                elif 'new_graph_is_weighted' in new_graph_checkboxes:
                    G = Graph( # directed, weighted, not acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), weighted= True),
                        weighted= True,
                        digraph= True,
                        layout= random_layout)
                elif 'new_graph_is_acyclic' in new_graph_checkboxes:
                    G = Graph( # directed, unweighted, acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), acyclic= True),
                        weighted= False,
                        digraph= True,
                        layout= random_layout)
                else:
                    G = Graph( # directed, unweighted, not acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), weighted= False, acyclic= True),
                        weighted= False,
                        digraph= True,
                        layout= random_layout)
            else:
                if 'new_graph_is_weighted' in new_graph_checkboxes and 'new_graph_is_acyclic' in new_graph_checkboxes: 
                    G = Graph( # undirected, weighted, acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False, weighted= True, acyclic= True),
                        weighted= True,
                        digraph= False,
                        layout= random_layout)
                elif 'new_graph_is_weighted' in new_graph_checkboxes: 
                    G = Graph( # undirected, weighted, not acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False, weighted= True),
                        weighted= True,
                        digraph= False,
                        layout= random_layout)
                elif 'new_graph_is_acyclic' in new_graph_checkboxes: 
                    G = Graph( # undirected, unweighted, acyclic
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False, acyclic= True),
                        weighted= False,
                        digraph= False,
                        layout= random_layout)
                else: 
                    G = Graph( # undirected, unweighted
                        erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False),
                        weighted= False,
                        digraph= False,
                        layout= random_layout)
            return G.elements, G.to_dict(), G.stylesheet, random_layout

