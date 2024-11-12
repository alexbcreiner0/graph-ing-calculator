from numpy import random as r
from dash import Dash, html, dcc, callback, Input, Output, ctx
import dash_cytoscape as cyto
import plotly.express as px
import string
from dash.exceptions import PreventUpdate

# How to use: 
# To make a new graph, just type G = Graph(args). 
# The arguments for the constructor can be any of the following:
# 	Nothing (can fill in nodes and edges with future method calls)
# 	A list of ordered pairs representing edges. (Vertex names can be any literal.)
#  	A dictionary representing an adjacency list
 
app = Dash(__name__)
cyto.load_extra_layouts()
extra_edges = False

class Graph:
	def __init__(self, arg = None, digraph = True, weighted = False,
					ident = 'graph', layout = 'circle'):
		self.is_directed = digraph

		self.identifier = ident
		self.layout = {'name': layout}
		self.style = {'width': '100%', 'height': '900px'}
		self.elements = []
		self.stylesheet = [{'selector': 'node', 'style': {'label': 'data(label)'}},
			{'selector': '.back', 'style': {'line-color': 'red', 'target-arrow-color': 'red'}},
			{'selector': '.forward', 'style': {'line-color': 'blue', 'target-arrow-color': 'blue'}},
			{'selector': '.cross', 'style': {'line-color': 'green', 'target-arrow-color': 'green'}}]
		if self.is_directed:
			style = {'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'label': 'data(label)'}
			self.stylesheet.append({'selector': 'edge', 'style': style})

		if type(arg) == dict:
			self.adj_list = arg
			self.__patch_list()
			self.vertices = list(self.adj_list.keys())
			self.edges = []
			for key, item in self.adj_list.items():
				for dest in item:
					self.edges.append((key,dest))
		else:
			if arg == None:
				arg = []
			self.edges = arg
					
		if type(arg) != dict:
			self.adj_list = {}
			self.vertices = []
			# make vertices
			for edge in self.edges:
				if edge[0] not in self.vertices:
					self.vertices.append(edge[0])
				if edge[1] not in self.vertices:
					self.vertices.append(edge[1])
			# make adjacency list
			for start, end in self.edges:
				if start in self.adj_list:
					if end not in self.adj_list[start]:
						self.adj_list[start].append(end)
				else:
					self.adj_list[start] = [end]
			# add entries for terminal nodes
			for vertex in self.vertices:
				if vertex not in self.adj_list:
					self.adj_list[vertex] = []

		if not digraph: self.__undigraphify()
		self.__create_elements()

	def __patch_list(self):
		new_keys = []
		for neighbors in self.adj_list.values():
			new_keys += [node for node in neighbors
				if node not in self.adj_list.keys()]
		list_appending = {node: [] for node in set(new_keys)}
		self.adj_list.update(list_appending)

	def __undigraphify(self):
		new_edges = []
		for edge in self.edges:
			reverse = (edge[1],edge[0])
			if reverse not in self.edges:
				new_edges.append(reverse)
		self.edges += new_edges
		for edge in new_edges:
			if edge[1] not in self.adj_list[edge[0]]:
				self.adj_list[edge[0]].append(edge[1])

	def __create_elements(self):
		self.vertex_directory = {}
		self.edge_directory = {}
		counter = 0
		for v in self.vertices:
			data = {'id': str(v), 'label': str(v)}
			node = {'data': data, 'grabbable': True, 'selectable': True}
			self.elements.append(node)
			self.vertex_directory[str(v)] = counter
			counter += 1
		for edge in self.edges:
			edge_data = {'id': str(edge[0])+str(edge[1]),
			 'source': str(edge[0]), 'target': str(edge[1])}
			self.elements.append({'data': edge_data})
			self.edge_directory[str(edge[0])+str(edge[1])] = counter
			counter += 1

	def __str__(self):
		return str(self.adj_list)

	def add_edge(self, edge, second = False):
		if edge[0] not in self.vertices:
			self.vertices.append(str(edge[0]))
			data = {'id': str(edge[0]), 'label': str(edge[0])}
			node = {'data': data, 'grabbable': True, 'selectable': True}
			self.elements.append(node)
			self.vertex_directory[edge[0]] = len(self.elements)-1
		if edge[1] not in self.vertices:
			self.vertices.append(str(edge[1]))
			data = {'id': str(edge[1]), 'label': str(edge[1])}
			node = {'data': data, 'grabbable': True, 'selectable': True}
			self.elements.append(node)
			self.vertex_directory[edge[1]] = len(self.elements)-1
		if edge not in self.edges:
			self.edges.append(edge)
			if edge[0] not in self.adj_list:
				self.adj_list[edge[0]] = [edge[1]]
			else:
				self.adj_list[edge[0]].append(edge[1])
			
			edge_data = {'id': str(edge[0])+str(edge[1]),
			 'source': str(edge[0]), 'target': str(edge[1])}
			self.elements.append({'data': edge_data})
			self.edge_directory[str(edge[0])+str(edge[1])] = len(self.elements)-1

		self.__patch_list()
		if not self.is_directed and not second: self.add_edge((edge[0], edge[1]), True)

	def add_vertex(self, vertex):
		if vertex not in self.vertices:
			self.vertices.append(vertex)
			self.adj_list[vertex] = []
			data = {'id': str(vertex), 'label': str(vertex)}
			node = {'data': data, 'grabbable': True, 'selectable': True}
			self.elements.append(node)

	def classify_edge(self, edge, edge_type):
		index = self.edge_directory[str(edge[0])+str(edge[1])]
		self.elements[index]['classes'] = edge_type

	def get_elements(self):
		return self.elements

	def get_stylesheet(self):
		return self.stylesheet

	def display(self):
		get_layout(self)

#G = Graph([('A','B'), ('A','F'), ('B','C'), ('B','E'), ('C','D'), ('D','B'), ('D','H'), ('E','D'), ('E','G'), ('F','E'), ('F','G'), ('G','F'),('H','G')])
# G = Graph({
# 	'A': ['B', 'C'],
# 	'B': ['E'],
# 	'C': ['D', 'E'],
# 	'D': ['B', 'F'],
# 	'E': ['F'],
# 	'F': ['A']
# })
# G = Graph({
# 	'A': ['B'],
# 	'B': ['D'],
# 	'C': ['A', 'D'],
# 	'D': []
# })
# G = Graph({
# 	'A': ['B', 'D'],
# 	'B': ['C', 'E'],
# 	'C': ['F'],
# 	'D': ['H'],
# 	'E': ['A', 'H'],
# 	'F': ['I'],
# 	'G': ['D'],
# 	'H': ['G', 'F', 'I'],
# 	'I': ['H']
# 	})

# G = Graph({
# 	'A': ['B', 'D'],
# 	'B': ['E'],
# 	'C': ['I', 'E', 'H'],
# 	'D': ['C', 'I', 'E'],
# 	'E': [],
# 	'G': ['H'],
# 	'F': ['G', 'J'],
# 	'H': [],
# 	'I': [],
# 	'J': []
# })

G = Graph({
	'A': ['B', 'E'],
	'B': ['A', 'F'],
	'C': ['F', 'G', 'D'],
	'D': ['C', 'G', 'H'],
	'E': [],
	'F': ['G'],
	'G': ['H']
	}, digraph= False)

def random_graph(n, m, digraph = True):
	# make random adjacency list
	letters = list(string.ascii_uppercase)
	p = m/(n-1)
	adj_list = {letters[i]: [] for i in range(n)}
	rng = r.default_rng()
	for i in adj_list:
		for j in range(n):
			if letters[j] == i: continue
			if rng.binomial(1, p) == 1:
				adj_list[i].append(letters[j])
	G = Graph(adj_list, digraph = digraph)
	return G

def pre_post(G, display_extra_edges = False):
	def dfs_explore(u, visited, clock, pre, post, G, H = None, pred = None):
		if H == None:
			H = Graph()
		visited[u] = True
		pre[u] = clock
		clock += 1
		if pred:
			H.add_edge((pred, u))
		for nbr in G.adj_list[u]:
			if not visited[nbr]:
				clock, H = dfs_explore(nbr, visited, clock, pre, post, G, H, u)
		post[u] = clock
		clock += 1
		return clock, H

	H = Graph(digraph = G.is_directed)
	visited = {v: False for v in G.vertices}
	clock = 1
	pre = {v: None for v in G.vertices}
	post = {v: None for v in G.vertices}

	for u in G.vertices:
		if not visited[u]:
			clock, tree = dfs_explore(u, visited, clock, pre, post, G)
			for edge in tree.edges:
				H.add_edge(edge)

	for v in visited:
		if v not in H.adj_list:
			H.add_vertex(v)

	new_adj_list = {}
	for v in visited:
		new_v = v + ': '+str(pre[v])+','+str(post[v])
		new_adj_list[new_v] = []
		nbr_list = H.adj_list[v]
		for nbr in nbr_list:
			new_adj_list[new_v].append(str(nbr)+': '+str(pre[nbr])+','+str(post[nbr]))

	if display_extra_edges: old_edge_names = H.edges
	H = Graph(new_adj_list, digraph = G.is_directed)
	
	if display_extra_edges:
		extra_edges = list(set(G.edges).difference(set(old_edge_names)))
		for edge in extra_edges:
			u,v = edge[0], edge[1]
			u_x = str(u)+': '+str(pre[u])+','+str(post[u])
			v_x = str(v)+': '+str(pre[v])+','+str(post[v])
			H.add_edge((u_x,v_x))
			if pre[v] < pre[u] and post[u] < post[v]:
				H.classify_edge((u_x,v_x), 'back')
			elif pre[u] < pre[v] and post[v] < post[u]:
				H.classify_edge((u_x,v_x), 'forward')
			else:
				H.classify_edge((u_x,v_x), 'cross') 
	return H

def is_connected(G):
	def dfs_explore(u, visited, ccnum):
		visited[u] = True
		ccnums[u] = ccnum
		for v in G.adj_list[u]:
			if not visited[v]: 
				dfs_explore(v, visited, ccnum)

	ccnum = 0
	visited = {v: False for v in G.vertices}
	ccnums = {str(v): False for v in G.vertices}
	for v in G.vertices:
		if not visited[v]:
			ccnum += 1
			dfs_explore(v, visited, ccnum)

	new_adj_list = {}
	for v in ccnums:
		new_v = v + ': ' + str(ccnums[v])
		new_adj_list[new_v] = []
		nbr_list = G.adj_list[v]
		for nbr in nbr_list:
			new_adj_list[new_v].append(str(nbr)+': '+str(ccnums[str(nbr)]))
	H = Graph(new_adj_list, digraph = G.is_directed)
	return H

@callback(Output(component_id='graph', component_property='layout', allow_duplicate=True), 
	Input('layout dropdown', 'value'), 
	prevent_initial_call='initial_duplicate')
def update_layout(layout):
	if ctx.triggered_id == None: raise PreventUpdate
	return {'name': layout, 'animate': True}

@callback(Output('dummy', 'children'), Input(component_id='extra_edges', component_property='value'))
def change_extra_edges(value):
	if ctx.triggered_id == None: raise PreventUpdate
	print(value)
	global extra_edges
	if len(value) == 0: extra_edges = False
	if len(value) == 1: extra_edges = True
	return ''

@callback(Output(component_id='graph', component_property='elements'),
	Output('graph', 'layout'),
	Input(component_id='random_button', component_property='n_clicks'),
	Input(component_id='nodes', component_property='value'),
	Input(component_id='avg_edges', component_property='value'),
	Input(component_id='dfs_forest', component_property='n_clicks'),
	Input(component_id='layout dropdown', component_property='value'),
	Input(component_id='connectedness', component_property='n_clicks')
	)
def new_graph(random_button, nodes, avg_edges, dfs_button, layout, connected_button):
	print(ctx.triggered_id)
	if ctx.triggered_id == None: raise PreventUpdate
	global G
	global extra_edges
	if ctx.triggered_id == 'dfs_forest':
		H = pre_post(G, extra_edges)
		return H.get_elements(), {'name': layout, 'animate': True}
	elif ctx.triggered_id == 'nodes':
		try:
			nodes = int(nodes)
			if nodes <= 1: raise PreventUpdate
			G = random_graph(int(nodes), int(avg_edges))
			return G.get_elements(), {'name': layout, 'animate': True}
		except ValueError:
			raise PreventUpdate
	elif ctx.triggered_id == 'avg_edges':
		try:
			avg_edges = float(avg_edges)
			G = random_graph(int(nodes), int(avg_edges))
			return G.get_elements(), {'name': layout, 'animate': True}
		except ValueError:
			raise PreventUpdate
	elif ctx.triggered_id == 'random_button':
		G = random_graph(int(nodes), int(avg_edges))
		return G.get_elements(), {'name': layout, 'animate': True}
	elif ctx.triggered_id == 'connectedness':
		H = is_connected(G)
		return H.get_elements(), {'name': layout, 'animate': True}

def get_layout(graph):
	global G
	G = graph
	layout_1=[]
	graph_layout=[]

	# create dropdown
	options_list = ['grid', 'random', 'circle', 'cose', 'concentric', 'dagre']
	options = [{'label': name.capitalize(), 'value': name} for name in options_list]
	dropdown = dcc.Dropdown(id='layout dropdown', value='circle', clearable=False, options=options)

	# create buttons
	button_1 = html.Button('Random Graph', id='random_button')
	button_2 = html.Button('dfs', id='dfs_forest')
	button_3 = html.Button('connectedness', id='connectedness')

	extra_edges_box = dcc.Checklist(['Display extra edges'], id='extra_edges')

	# create graph component
	layout = {'name': 'dagre'}
	style = {'width': '700', 'height': '700px'}
	elements = G.get_elements()
	stylesheet = G.get_stylesheet()
	graph_component=cyto.Cytoscape(id='graph', layout=layout, style=style, elements=elements, stylesheet=stylesheet)

	graph_layout.append(graph_component)
	control_layout_children_1 = [dropdown]
	control_layout_children_2 = [button_1, button_2, extra_edges_box, button_3]
	control_layout_children_3 = [html.H3('No. nodes: '), dcc.Input(id='nodes', value='7', type='text')]
	control_layout_children_4 = [html.H3('Average edges per node: '), dcc.Input(id='avg_edges', value='2', type='text')]

	control_layout_1 = html.Div(control_layout_children_1, style={'flex_direction': 'row'})
	control_layout_2 = html.Div(control_layout_children_2, style={'display': 'flex', 'flex_direction': 'row'})
	control_layout_3 = html.Div(control_layout_children_3, style={'display': 'flex', 'flex_direction': 'row'})
	control_layout_4 = html.Div(control_layout_children_4, style={'display': 'flex', 'flex_direction': 'row'})
	dummy = html.Div(id='dummy', style={'display': 'none'})

	overall_layout = html.Div(children=[html.Div(graph_layout), control_layout_1, control_layout_2, control_layout_3, control_layout_4, dummy])

	global app
	app.layout = overall_layout
	app.run(debug=True)

if __name__ == '__main__':
	get_layout(G)
