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

def erdos_renyi_random_graph_old(n,m, directed= True, weighted = False, max_weight= 10, negative_weights= False, acyclic= False):
    letters = get_names(n)
    adj_list = { letter: {} for letter in letters } if weighted else { letter: [] for letter in letters }
    if directed:
        edges = [(letters[i], letters[j]) for i in range(n) for j in range(n) if i != j]
    else:
        edges = [(letters[i], letters[j]) for i in range(n) for j in range(i) if i != j]
    edge_sample = random.sample(edges, m)
    if negative_weights:
        weights = [ random.randint(-1*max_weight, max_weight) for i in range(m) ]
    else:
        weights = [ random.randint(1, max_weight) for i in range(m) ]
    for edge in edge_sample:
        if weighted:
            adj_list[edge[0]][edge[1]] = weights.pop()
        else:
            adj_list[edge[0]].append(edge[1])
    return adj_list

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            self.parent[rootY] = rootX
            return True
        return False


# Clever disjoint set data structure using union-by-rank and path compression
class DisjointFamily:
    def __init__(self, things = []):
        self.elements = {thing: thing for thing in things}
        self.ranks = {thing: 1 for thing in things} 

    def find_set(self, value):
        if value != self.elements[value]: 
            self.elements[value] = self.find_set(self.elements[value]) 
        return self.elements[value]

    def union(self, x, y):
        head_x = self.find_set(x)
        head_y = self.find_set(y)
        if head_x == head_y: return False
        if self.ranks[head_x] > self.ranks[head_y]:
            self.elements[head_y] = head_x
        else:
            self.elements[head_x] = head_y
            if self.ranks[head_x] == self.ranks[head_y]:
                self.ranks[head_y] = self.ranks[head_x]+1
        return True

def erdos_renyi_random_graph(n,m, directed= True, weighted = False, max_weight= 10, negative_weights= False, acyclic= False):
    letters = get_names(n)
    print(f"letters: {letters}")
    adj_list = { letter: {} for letter in letters } if weighted else { letter: [] for letter in letters }
    print(adj_list)
    if directed and acyclic:
        if weighted:
            adj_list = random_weighted_dag(n)
        else:
            adj_list = random_dag(n)
        return adj_list
        # print("directed and acyclic")
        # edges = [(letters[i], letters[j]) for j in range(n) for i in range(j) if i != j]
        # print(edges)
        # random.shuffle(edges)
        # edges_sample = edges[:m]
    elif directed and not acyclic:
        edges = [(letters[i], letters[j]) for i in range(n) for j in range(n) if i != j]
        random.shuffle(edges)
        edges_sample = edges[:m]
    elif not directed and acyclic:
        prelim_edges = [(letters[i], letters[j]) for i in range(n) for j in range(i) if i != j]
        random.shuffle(prelim_edges)
        dj = DisjointFamily(letters)
        edges_sample = []
        for edge in prelim_edges:
            if dj.union(edge[0],edge[1]):
                edges_sample.append(edge)
            if len(edges_sample) == m: break
    else: # undirected, not necessarily acyclic
        edges_sample = random.sample([(letters[i], letters[j]) for i in range(n) for j in range(i) if i != j],m)

    # generate weights if needed
    if negative_weights:
        weights = [ random.randint(-1*max_weight, max_weight) for i in range(m) ]
    else:
        weights = [ random.randint(1, max_weight) for i in range(m) ]
    for edge in edges_sample:
        if weighted:
            adj_list[edge[0]][edge[1]] = weights.pop()
        else:
            adj_list[edge[0]].append(edge[1])
    return adj_list

if __name__ == "__main__":
    print(erdos_renyi_random_graph(8, 10, directed= False, weighted= True, acyclic= True))
