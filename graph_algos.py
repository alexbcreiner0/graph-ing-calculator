from graphs import *

# returns the tree produced from exploring from a node
def explore_graph(vertex, G, visited = None, predecessor = None, H = None):
	if H == None:
		H = Graph()
	if visited == None:
		visited = {}
		for key in G.vertices:
			visited[key] = False
	visited[vertex] = True
	if predecessor:
		H.add_edge((predecessor, vertex))
	for neighbor in G.adj_list[vertex]:
		if not visited[neighbor]:
			explore_graph(neighbor, G, visited, predecessor = vertex, H = H)
	return H

# returns the forest produced from calling explore_graph on every possible node
def dfs_graph(G, visited = None, H = None):
	if H == None:
		H = Graph(digraph = G.is_directed)
	if visited == None:
		visited = {}
		for vertex in G.vertices:
			visited[vertex] = False
	for vertex in G.vertices:
		if not visited[vertex]:
			tree = explore_graph(vertex, G, visited)
			for edge in tree.edges:
				H.add_edge(edge)
	return H

def is_cyclic(G):
	pre, post, tree_edges = pre_post(G)
	for edge in G.edges:
		if edge not in tree_edges:
			if pre[edge[1]] < pre[edge[0]] and post[edge[0]] < post[edge[1]]:
				return True
	return False

def is_connected(G, get_nums = False):
	def dfs_explore(u, visited, ccnum, G):
		visited[u] = True
		ccnums[u] = ccnum
		for v in G.adj_list[u]:
			if not visited[v]:
				dfs_explore(v, visited, ccnum, G)

	ccnum = 0
	ccnums = {v: None for v in G.vertices}
	visited = {v: False for v in G.vertices}
	for v in G.vertices:
		if not visited[v]:
			ccnum += 1
			dfs_explore(v, visited, ccnum, G)

	if ccnum > 1:
		if get_nums: return False, ccnums
		else: return False
	else: 
		if get_nums: return True, ccnums
		else: return True

def pre_post(G):
	def dfs_explore(u, visited, clock, pre, post, G, tree_edges, pred = None):
		visited[u] = True
		pre[u] = clock
		clock += 1
		if pred:
			tree_edges.append((pred,u))
		for v in G.adj_list[u]:
			if not visited[v]:
				clock, tree_edges = dfs_explore(v, visited, clock, pre, post, G, tree_edges, u)
		post[u] = clock
		clock += 1
		return clock, tree_edges

	clock = 1
	visited = {v: False for v in G.vertices}
	pre = {v: None for v in G.vertices}
	post = {v: None for v in G.vertices}
	tree_edges = []
	for u in G.vertices:
		if not visited[u]:
			clock, tree_edges = dfs_explore(u, visited, clock, pre, post, G, tree_edges)

	return pre, post, tree_edges

def topo_sort(G):
	if is_cyclic(G):
		print('Task is impossible.')
		return None
	else:
		pre, post, tree_edges = pre_post(G)
		flipped = {item: key for key, item in post.items()}
		sorted_keys = sorted(flipped, reverse = True)
		linearized = [flipped[k] for k in sorted_keys]
		return linearized

if __name__ == '__main__':
	G = Graph({'A': ['C'], 'B': ['A', 'D'], 'C': ['E', 'F'], 'D': ['C']})
	print(topo_sort(G))
	G.display()

	# Fig 3.2 graph 
	#G = Graph([('A','B'),('A','C'), ('B','F'), ('B','E'), ('C','F'),('D','A'),('E','I'),('E','J'), ('G','D'),('G','H'), ('H','D'),('I','J'),('K','L')], digraph = False)
	# fig 3.7 graph
	#G = Graph([('A','B'), ('A','C'),('A','F'), ('B','E'),('C','D'),('D','A'),('D','H'),('E','F'),('E','G'),('E','H'),('F','G'),('F','B'),('H','G')], digraph = True)
	# fig 3.6 graph
	# G = Graph({'A': ['B','E'], 'E': ['I','J'], 'I': ['J'], 'C': ['D','H','G'], 'G': ['H','K'], 'K': ['H'], 'H': ['L', 'D'], 'F': []}, digraph = False)	# A = random_graph(5,2, digraph = True)
	# fig 3.8 graph