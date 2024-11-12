from dash import Dash, html, dcc
import dash_cytoscape as cyto
from graph_examples import *
from graph_generators import *
from settings import *
from graph import Graph
from callbacks import register_callbacks

app = Dash(__name__, title= 'Visual Graphing Calculator')

G: Graph = Graph(G_unknown)
# G: Graph = Graph(digraph= True, weighted= True)
register_callbacks(app)

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
                value='grid', 
                clearable=False, 
                options=options_list,
                style={'flex-grow': '1'}
            )
        ],
        style= {'display': 'flex', 'flex_direction': 'row', 'align-items': 'center'}
    )
    return dropdown_row

def get_new_graph_row():
    return html.Div(
        [
            html.Button( 'New Graph', id= 'new_graph_button', style={'margin-right': '5px'} )
        ],
        style={'display': 'flex', 'align-items': 'center'}
    )

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

if __name__ == '__main__':
    import json
    print(G.to_dict())
    try:
        json.dumps(vars(G))
        print("G's properties are JSON-serializable.")
    except TypeError as e:
        print("Found non-serializable data in G:", e)
    cyto.load_extra_layouts()
    # extra_edges = False

    graph_display = html.Div(G.get_cytograph())
    dropdown_row = get_dropdown_row()
    add_elements_row = get_graph_edit_row()
    new_graph_row = get_new_graph_row()
    title = html.H1("'Graphing' Calculator")
    graph_store = dcc.Store(id= 'current_graph', data= G.to_dict())
    # remove_elements_row = get_graph_remove_row()

    display_panel = html.Div(
        children= [ graph_display ],
        style={'flex': '2', 'padding': '10px'}
    )

    control_panel = html.Div(
        children= [ title, dropdown_row, add_elements_row, new_graph_row ],
        style={'flex': '1', 'padding': '10px'}
    )

    app.layout = html.Div(
        children= [ graph_store, control_panel, display_panel ],
        style= { 'display': 'flex', 'flex-direction': 'row', 'gap': '20px', 'min-height': '100vh' }
    )

    app.run(debug= True)
    
# Old layout in case the new fancy one fails
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
