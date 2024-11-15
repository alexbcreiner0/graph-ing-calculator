from dash import Input, Output, ctx
from random import randint
from dash.dependencies import extract_callback_args
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

def make_dfs_forest(adj_list, is_directed= True, is_weighted= False):
    print(f"Directed: {is_directed}")
    G, G_extra = depth_first_traverse(adj_list, display_extra_edges= True, is_weighted = is_weighted, is_directed= is_directed)
    return G, G_extra

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
                  Output(component_id='extra_info', component_property='data'),
                  #Output(component_id='layout dropdown', component_property='value'),
                  Input(component_id='current_graph', component_property='data'),
                  Input(component_id='extra_info', component_property='data'),
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
                  Input(component_id='dfs_button', component_property='n_clicks'),
                  Input(component_id='display_extra_edges', component_property='value'))
    def add_new_edge(current_graph, extra_info, add_edge, new_edge_source_field, new_edge_dest_field, new_edge_weight_field, remove_edge, add_vertex, remove_vertex, vertex_name, new_graph_button, num_nodes_field_new_graph, num_edges_field_new_graph, new_graph_checkboxes, dfs_button, display_extra_edges):
        # print(ctx.triggered_id)
        if ctx.triggered_id in [None, 'extra_info', 'new_graph_checkboxes', 'current_graph', 'num_edges_field_new_graph', 'num_nodes_field_new_graph', 'new_edge_source_field', 'new_edge_dest_field', 'new_edge_weight_field', 'vertex_name']: raise PreventUpdate
        elif ctx.triggered_id == 'add_edge':
            G = add_edge_to_graph(
                current_graph['adj_list'], (new_edge_source_field, new_edge_dest_field),
                current_graph['is_directed'], current_graph['is_weighted'],
                current_graph['layout'], new_edge_weight_field)
            return G.elements, G.to_dict(), G.stylesheet, extra_info#, current_graph['layout']['name']
        elif ctx.triggered_id == 'remove_edge':
            G = remove_edge_from_graph(
                current_graph['adj_list'], (new_edge_source_field, new_edge_dest_field),
                current_graph['is_directed'], current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet, extra_info#, current_graph['layout']['name']
        elif ctx.triggered_id == 'add_vertex':
            G = add_vertex_to_graph(
                current_graph['adj_list'], vertex_name,
                current_graph['is_directed'], current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet, extra_info#, current_graph['layout']['name']
        elif ctx.triggered_id == 'remove_vertex':
            G = remove_vertex_from_graph(
                current_graph['adj_list'], vertex_name,
                current_graph['is_directed'], current_graph['is_weighted'])
            return G.elements, G.to_dict(), G.stylesheet, extra_info#, current_graph['layout']['name']
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
            G = create_new_graph(num_nodes, num_edges, new_graph_checkboxes, random_layout)
            extra_info['dfs_mode'] = False
            return G.elements, G.to_dict(), G.stylesheet, extra_info#, random_layout
        elif ctx.triggered_id == 'dfs_button':
            G, G_extra = make_dfs_forest(current_graph['adj_list'], is_weighted= current_graph['is_weighted'], is_directed= current_graph['is_directed'])
            extra_info['dfs_mode'] = True
            extra_info['reserve_vanilla_graph'] = G.to_dict()
            extra_info['reserve_fancy_graph'] = G_extra.to_dict()
            if display_extra_edges:
                return G_extra.elements, G_extra.to_dict(), G_extra.stylesheet, extra_info#, current_graph['layout']['name']            
            else:
                return G.elements, G.to_dict(), G.stylesheet, extra_info#, current_graph['layout']['name']            
        elif ctx.triggered_id == 'display_extra_edges':
            if extra_info['dfs_mode']:
                if 'display_extra_edges' in display_extra_edges:
                    G = Graph(extra_info['reserve_fancy_graph']['adj_list'], digraph= current_graph['is_directed'], weighted= current_graph['is_weighted'], layout= current_graph['layout']['name'])
                    G.elements = extra_info['reserve_fancy_graph']['elements']
                else:
                    G = Graph(extra_info['reserve_vanilla_graph']['adj_list'], digraph= current_graph['is_directed'], weighted= current_graph['is_weighted'], layout= current_graph['layout']['name'])
                    G.elements = extra_info['reserve_vanilla_graph']['elements']
                return G.elements, G.to_dict(), G.stylesheet, extra_info
            else:
                G = Graph(current_graph['adj_list'], digraph= current_graph['is_directed'], weighted= current_graph['is_weighted'], layout= current_graph['layout']['name'])
                return G.elements, G.to_dict(), G.stylesheet, extra_info

    
    @app.callback(Input(component_id="test_button", component_property="n_clicks"),
                  Input('extra_info', 'data'))
    def print_shit(text_button, extra_info):
        if ctx.triggered_id in [None, 'extra_info']: raise PreventUpdate
        mess = extra_info["reserve_dfs_graph"]["elements"]
        print([u['classes'] for u in mess if 'classes' in u])


