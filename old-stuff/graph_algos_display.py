from graphs import *

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

# returns the forest produces from calling explore_graph on every possible node,
# along with pre and post numbers labelled
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

if __name__ == '__main__':
	G = Graph({'A': [], 'B': ['C'], 'C': ['A', 'B'], 'D': [], 'E': ['B', 'F', 'G'], 'F': ['A', 'B'], 'G': ['A', 'C', 'F']})
	print(G)
	H = pre_post(G)
	H.display()
