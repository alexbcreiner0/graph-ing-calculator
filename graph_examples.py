G_unknown = {
    'A': {'B': 1, 'E': 4, 'F': 8},
    'B': {'C': 2, 'F': 6, 'G': 6},
    'C': {'D': 1, 'G': 2},
    'D': {'G': 1, 'H': 4},
    'E': {'F': 5},
    'F': {},
    'G': {'F': 1, 'H': 1},
    'H': {}
}

# 3.6 graph
G_3_6 = {
	'A': ['B','E'],
	'B': ['A'], 
	'C': ['D','H','G'],
	'D': ['C','H'],
	'E': ['A','I','J'],
	'F': [],
	'G': ['C','H','K'],
	'H': ['C','G','K','L'],
	'I': ['E','J'],
	'J': ['I','E'], 
	'K': ['G','H'],
	'L': ['H']
}

# 3.7 graph
G_3_7 = {
	'A': ['B','C'],
	'B': ['E'],
	'C': ['D'],
	'D': ['A'],
	'E': ['F','G','H'],
	'F': ['B','G'],
	'G': [],
	'H': ['G']
}

# 3.8 Graph
G_3_8 = {
	'A': ['C'],
	'B': ['A','D'],
	'C': ['E','F'],
	'D': ['C'],
	'E': [],
	'F': [],
}

# 3.10 Graph
G_3_10 = {
	'A': [],
	'B': ['A','E'],
	'C': ['B','F'],
	'D': ['B'],
	'E': ['B'],
	'F': ['E','C'],
	'G': ['E','I'],
	'H': ['F','G'],
	'I': ['J'],
	'J': ['G','L'],
	'K': ['H'],
	'L': ['K']
}

# 5.3 Graph (non-directed, redundant directions present)
G_5_3 = {
    'A': {'B': 2, 'C': 1},
    'B': {'A': 2, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 2, 'E': 3},
    'D': {'B': 1, 'C': 2, 'E': 3, 'F': 4},
    'E': {'C': 3, 'D': 3, 'F': 1},
    'F': {'D': 4, 'E': 1}
}

# 5.3 graph (non-directed, no redundancies)
G = {
    'A': {'B': 2, 'C': 1},
    'B': {'C': 2, 'D': 1},
    'C': {'D': 2, 'E': 3},
    'D': {'E': 3, 'F': 4},
    'E': {'F': 1},
    'F': {}
}
