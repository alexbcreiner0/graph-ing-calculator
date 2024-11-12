# THIS ONE IS THE NEWEST
import heapq

from graph_examples import G_3_10

def is_weighted(G):
	if len(G) == 0: return False
	for adj in G.values():
		if type(adj) == dict: return True
		break
	return False

def unweightify(G):
	new_G = {v: {} for v in G}
	for v in new_G:
		new_G[v] = [u for u in G[v].keys()]
	return new_G

def pre_post(G, get_tree_edges = False):
	def explore(G, u, visited, pre, post, clock, tree_edges):
		visited[u] = True
		for v in G[u]:
			if not visited[v]:
				tree_edges.append((u,v))
				clock += 1
				pre[v] = clock
				clock = explore(G, v, visited, pre, post, clock, tree_edges)
				clock += 1
				post[v] = clock
		return clock

	pre, post = {u: None for u in G}, {u: None for u in G}
	visited = {u: False for u in G}
	tree_edges = []
	clock = 0
	for u in G:
		if not visited[u]:
			clock += 1
			pre[u] = clock
			clock = explore(G, u, visited, pre, post, clock, tree_edges)
			clock += 1
			post[u] = clock

	if get_tree_edges:
		return pre, post, tree_edges
	return pre, post

def reverse(G):
	rev_G = {u: [] for u in G}
	for u in G:
		for v in G[u]:
			rev_G[v].append(u)
	return rev_G

def is_cyclic(G):
	if is_weighted(G):
		G = unweightify(G)
	pre, post, tree_edges = pre_post(G, get_tree_edges=True)
	non_tree_edges = []
	for u in G:
		for v in G[u]:
			if not (u,v) in tree_edges:
				non_tree_edges.append((u,v))
	
	for edge in non_tree_edges:
		if pre[edge[1]] < pre[edge[0]] and post[edge[0]] < post[edge[1]]:
			return True
	return False

def topo_sort(G):
	if is_weighted(G):
		G = unweightify(G)
	pre, post = pre_post(G)
	flipped_dict = [(-1*p, node) for (node, p) in post.items()]
	heapq.heapify(flipped_dict)
	return [heapq.heappop(flipped_dict)[1] for i in range(len(G))]

def connectedness(G, node_order = None):
	def explore(G, u, visited, ccnum, ccnums, node_order):
		visited[u] = True
		ccnums[u] = ccnum
		for v in G[u]:
			if not visited[v]:
				explore(G, v, visited, ccnum, ccnums, node_order)

	if is_weighted(G):
		G = unweightify(G)
	ccnum, ccnums = 0, {u: 0 for u in G}
	visited = {u: False for u in G}

	if node_order == None:
		node_order = [u for u in G]

	for u in node_order:
		if not visited[u]:
			ccnum += 1
			explore(G, u, visited, ccnum, ccnums, node_order)

	return ccnum, ccnums

def strong_connectedness(G):
	if is_weighted(G):
		G = unweightify(G)
	rev_G = reverse(G)
	sorted_nodes = topo_sort(rev_G)
	return connectedness(G, sorted_nodes)

if __name__ == '__main__':
	print(strong_connectedness(G_3_10))
