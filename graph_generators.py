import math
from dfs_algos import *
from numpy import random as r
import random

def lexicographic(n_chars):
    if n_chars == 1:
        return [chr(i+65) for i in range(26)]
    else:
        shorter_strings = lexicographic(n_chars-1)
        new_strings = []
        for string in shorter_strings:
            new_strings += [string+chr(i+65) for i in range(26)]
        return new_strings

def get_names(n):
    names = []
    i = 1
    while len(names) < n:
        names += lexicographic(i)
        i += 1
    return names[:n]

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

def erdos_renyi_random_graph_old(n,m):
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
    return adj_list

def erdos_renyi_random_graph(n,m, directed= True):
    # helper method to generate all n^2 possible edge pairs
    letters = get_names(n)
    print(letters)
    adj_list = { letter: [] for letter in letters }
    if directed:
        edges = [(letters[i], letters[j]) for i in range(n) for j in range(n) if i != j]
    else:
        edges = [(letters[i], letters[j]) for i in range(n) for j in range(i) if i != j]
    edge_sample = random.sample(edges, m)
    for edge in edge_sample:
        adj_list[edge[0]].append(edge[1])
    return adj_list

if __name__ == "__main__":
    print(erdos_renyi_random_graph(10, 20, directed= False))
