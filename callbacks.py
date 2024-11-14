from dash import Input, Output, ctx
from random import randint
from dash.exceptions import PreventUpdate
from settings import *
from graph import Graph
from graph_generators import erdos_renyi_random_graph, random_graph
from graph_algos_new import depth_first_traverse

def add_edge_to_graph(adj_list, edge, is_directed, is_weighted, current_layout, weight= ''):
    source = edge[0]
    dest = edge[1]
    print(f'source = {source}, dest= {dest}')
    print(f'Weighted: {is_weighted}')
    if source not in adj_list:
        if is_weighted:
            adj_list[source] = {dest: float(weight)}
        else:
            adj_list[source] = [dest]
    else:
        if is_weighted:
            adj_list[source][dest] = float(weight) if weight != '' else 0.0
        else:
            adj_list[source].append(dest)
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

def create_new_graph(num_nodes, num_edges, new_graph_checkboxes, layout):
    if 'new_graph_is_directed' in new_graph_checkboxes:
        if 'new_graph_is_weighted' in new_graph_checkboxes and 'new_graph_is_acyclic' in new_graph_checkboxes:
            G = Graph( # directed, weighted, acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), weighted= True, acyclic= True),
                weighted= True,
                digraph= True,
                layout= layout)
            print(G.adj_list)
        elif 'new_graph_is_weighted' in new_graph_checkboxes:
            G = Graph( # directed, weighted, not acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), weighted= True),
                weighted= True,
                digraph= True,
                layout= layout)
        elif 'new_graph_is_acyclic' in new_graph_checkboxes:
            G = Graph( # directed, unweighted, acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), acyclic= True),
                weighted= False,
                digraph= True,
                layout= layout)
        else:
            G = Graph( # directed, unweighted, not acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), weighted= False, acyclic= False),
                weighted= False,
                digraph= True,
                layout= layout)
    else:
        if 'new_graph_is_weighted' in new_graph_checkboxes and 'new_graph_is_acyclic' in new_graph_checkboxes: 
            G = Graph( # undirected, weighted, acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False, weighted= True, acyclic= True),
                weighted= True,
                digraph= False,
                layout= layout)
        elif 'new_graph_is_weighted' in new_graph_checkboxes: 
            G = Graph( # undirected, weighted, not acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False, weighted= True),
                weighted= True,
                digraph= False,
                layout= layout)
        elif 'new_graph_is_acyclic' in new_graph_checkboxes: 
            G = Graph( # undirected, unweighted, acyclic
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False, acyclic= True),
                weighted= False,
                digraph= False,
                layout= layout)
        else: 
            G = Graph( # undirected, unweighted
                erdos_renyi_random_graph(int(num_nodes), int(num_edges), directed= False),
                weighted= False,
                digraph= False,
                layout= layout)
    return G

def make_dfs_forest(adj_list):
    G = depth_first_traverse(adj_list, display_extra_edges= True)
    return G

def register_callbacks(app):
    @app.callback(Output(component_id='graph', component_property='layout', allow_duplicate=True), 
        Input('layout dropdown', 'value'), 
        prevent_initial_call='initial_duplicate')
    def update_layout(layout):
        print(f"Changing layout. ctx triggered id: {ctx.triggered_id}")
        if ctx.triggered_id == None:
            raise PreventUpdate
        else:
            return LAYOUT_SETTINGS[layout]

    @app.callback(Output(component_id='graph', component_property='elements'),
                  Output(component_id='current_graph', component_property='data'),
                  Output(component_id='graph', component_property='stylesheet'),
                  #Output(component_id='layout dropdown', component_property='value'),
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
                  Input(component_id='new_graph_checkboxes', component_property='value'),
                  Input(component_id='dfs_button', component_property='n_clicks'))
    def add_new_edge(current_graph, add_edge, new_edge_source_field, new_edge_dest_field, new_edge_weight_field, remove_edge, add_vertex, remove_vertex, vertex_name, new_graph_button, num_nodes_field_new_graph, num_edges_field_new_graph, new_graph_checkboxes, dfs_button):
        # print(ctx.triggered_id)
        if ctx.triggered_id in [None, 'new_graph_checkboxes', 'current_graph', 'num_edges_field_new_graph', 'num_nodes_field_new_graph', 'new_edge_source_field', 'new_edge_dest_field', 'new_edge_weight_field', 'vertex_name']: raise PreventUpdate
        elif ctx.triggered_id == 'add_edge':
            print(f"{(new_edge_source_field, new_edge_dest_field)}")
            G = add_edge_to_graph(
                current_graph['adj_list'], (new_edge_source_field, new_edge_dest_field),
                current_graph['is_directed'], current_graph['is_weighted'],
                current_graph['layout'], new_edge_weight_field)
            return G.elements, G.to_dict(), G.stylesheet#, current_graph['layout']['name']
        elif ctx.triggered_id == 'remove_edge':
            G = remove_edge_from_graph(
                current_graph['adj_list'], (new_edge_source_field, new_edge_dest_field),
                current_graph['is_directed'], current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet#, current_graph['layout']['name']
        elif ctx.triggered_id == 'add_vertex':
            G = add_vertex_to_graph(
                current_graph['adj_list'], vertex_name,
                current_graph['is_directed'], current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet#, current_graph['layout']['name']
        elif ctx.triggered_id == 'remove_vertex':
            G = remove_vertex_from_graph(
                current_graph['adj_list'], vertex_name,
                current_graph['is_directed'], current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet#, current_graph['layout']['name']
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
            print(f"num nodes: {num_nodes}, num edges: {num_edges}, checkboxes: {new_graph_checkboxes}, layout: {random_layout}")
            G = create_new_graph(num_nodes, num_edges, new_graph_checkboxes, random_layout)
            return G.elements, G.to_dict(), G.stylesheet#, random_layout
        elif ctx.triggered_id == 'dfs_button':
            G = make_dfs_forest(current_graph['adj_list'])
            return G.elements, G.to_dict(), G.stylesheet#, current_graph['layout']['name']            
