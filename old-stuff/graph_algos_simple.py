from numpy import random as r
from dash import Dash, html, dcc, callback, Input, Output
import dash_cytoscape as cyto
from matplotlib import pyplot as plt
import plotly.express as px
import sys
import string
import dfs

# How to use: 
# To make a new graph, just type G = Graph(args). 
# The arguments for the constructor can be any of the following:
# 	Nothing (can fill in nodes and edges with future method calls)
# 	A list of ordered pairs representing edges. (Vertex names can be any literal.)
#  	A dictionary representing an adjacency list

app = Dash(__name__)
cyto.load_extra_layouts()

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
		app.layout = html.Div(cyto.Cytoscape(id = self.identifier, 
			layout = self.layout, style = self.style, stylesheet = self.stylesheet,
			elements = self.elements))
		app.run(debug= True)

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

@callback(Output('graph', 'layout'), Input('layout dropdown', 'value'))
def update_layout(layout):
	return {'name': layout, 'animate': True}

@callback(Output(component_id='graph', component_property='elements'), 
	Input(component_id='button', component_property='n_clicks'),
	Input(component_id='nodes', component_property='value'),
	Input(component_id='avg_edges', component_property='value'))
def new_graph(n_clicks, nodes, avg_edges):
	if avg_edges == '': avg_edges = 0
	if nodes == '': nodes = 0	
	G = random_graph(int(nodes),int(avg_edges))
	return G.get_elements()

if __name__ == '__main__':
	layout_1=[]
	graph_layout=[]

	# create dropdown
	options_list = ['grid', 'random', 'circle', 'cose', 'concentric', 'dagre']
	options = [{'label': name.capitalize(), 'value': name} for name in options_list]
	# options=[{'label': 'Grid', 'value': 'grid'}, {'label': 'Circle', 'value': 'circle'}]
	dropdown = dcc.Dropdown(id='layout dropdown', value='circle', clearable=False, options=options)

	# create button
	button_1 = html.Button('Random Graph', id='button')
	button_2 = html.Button('dfs', id='dfs_forest')


	# create graph component
	G = Graph({'A': ['B','E'], 'E': ['I','J'], 'I': ['J'], 'C': ['D','H','G'], 'G': ['H','K'], 'K': ['H'], 'H': ['L', 'D'], 'F': []}, digraph = False)
	layout = {'name': 'dagre'}
	style = {'width': '700', 'height': '700px'}
	elements = G.get_elements()
	stylesheet = G.get_stylesheet()
	graph_component=cyto.Cytoscape(id='graph', layout=layout, style=style, elements=elements, stylesheet=stylesheet)

	graph_layout.append(graph_component)
	control_layout_children_1 = [dropdown, button_1, button_2]
	control_layout_children_2 = [html.H3('No. nodes: '), dcc.Input(id='nodes', value='7', type='text')]
	control_layout_children_3 = [html.H3('Average edges per node: '), dcc.Input(id='avg_edges', value='2', type='text')]

	control_layout_1 = html.Div(control_layout_children_1, style={'display': 'flex', 'flex_direction': 'row'})
	control_layout_2 = html.Div(control_layout_children_2, style={'display': 'flex', 'flex_direction': 'row'})
	control_layout_3 = html.Div(control_layout_children_3, style={'display': 'flex', 'flex_direction': 'row'})

	overall_layout = html.Div(children=[html.Div(graph_layout), control_layout_1, control_layout_2, control_layout_3])

	app.layout = overall_layout

	app.run(debug=True)



	# Fig 3.2 graph 
	#G = Graph([('A','B'),('A','C'), ('B','F'), ('B','E'), ('C','F'),('D','A'),('E','I'),('E','J'), ('G','D'),('G','H'), ('H','D'),('I','J'),('K','L')], digraph = False)
	# fig 3.7 graph
	#G = Graph([('A','B'), ('A','C'),('A','F'), ('B','E'),('C','D'),('D','A'),('D','H'),('E','F'),('E','G'),('E','H'),('F','G'),('F','B'),('H','G')], digraph = True)
	# fig 3.6 graph
	# G = Graph({'A': ['B','E'], 'E': ['I','J'], 'I': ['J'], 'C': ['D','H','G'], 'G': ['H','K'], 'K': ['H'], 'H': ['L', 'D'], 'F': []}, digraph = False)	# A = random_graph(5,2, digraph = True)
