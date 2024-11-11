import math
import string
from dfs_algos import *
import time
from numpy import random as r

def lexicographic(n):
	max_length = math.ceil(math.log(n)/math.log(26))
	if n < 26:
		return [chr(i+97) for i in range(26)]
	else:
		A = []
		for i in range(26):
			A += [chr(i+97)+s for s in lexicographic(n//26)]
			if len(A) > n: break
		return lexicographic(n//26) + A

def matrix_to_list(adj_matrix):
	n = len(adj_matrix)
	letters = lexicographic(n)
	G = {letters[i]: [] for i in range(n)}
	for i,u in enumerate(G):
		for j in range(n):
			if adj_matrix[i][j] == 1:
				G[u].append(letters[j])
	return G

def random_graph(n):
	rng = r.default_rng()
	edge_count = 0
	for j in range(5):
		edge_count += int((n*r.random())**2)
	edge_count = int(edge_count/5)
	letters = lexicographic(n)
	graph = {letters[i]: [] for i in range(n)}
	for i in range(edge_count):
		source = letters[rng.integers(0,n)]
		sink = letters[rng.integers(0,n)]
		graph[source].append(sink)
		graph[source] = list(set(graph[source]))
	return graph

def random_weighted_graph(n, weight_range = (1,10), negative_weights = False):
	rng = r.default_rng()
	unweighted_graph = random_graph(n)
	graph = {u: {} for u in unweighted_graph}
	for u in graph:
		for v in unweighted_graph[u]:
			w = rng.integers(weight_range[0], weight_range[1])
			graph[u][v] = w
	return graph

# Works because a matrix is a dag iff it's nodes can be rearranged such that it's adjacency matrix is triangular (toposort a dag and see for yourself)
def random_dag(n):
	adj_matrix = [[0]*n for i in range(n)]
	rng = r.default_rng()
	for i in range(n):
		for j in range(i+1,n):
			adj_matrix[i][j] = round(rng.random())
	return adj_matrix

def random_weighted_dag(n, weight_range = (1,10), negative_weights = False):
	rng = r.default_rng()
	unweighted_graph = matrix_to_list(random_dag(n))
	graph = {u: {} for u in unweighted_graph}
	for u in graph:
		for v in unweighted_graph[u]:
			w = rng.integers(weight_range[0], weight_range[1])
			graph[u][v] = w
	return graph
