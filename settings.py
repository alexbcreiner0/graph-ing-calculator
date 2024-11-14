import random

LAYOUT_SETTINGS = {
    'cose': { 'name': 'cose', 'nodeRepulsion': 400000000, 'idealEdgeLength': 100, 'nodeOverlap': 200, 
        'edgeElasticity': 0.45, 'padding': 30, 'animate': True, 'animationEasing': 'ease-in-out', 'animationDuration': 1000000, 'animationThreshold': 0 },
    'circle': {'name': 'circle', 'animate': True},
    'concentric': {'name': 'concentric', 'minNodeSpacing': 100, 'equidistant': True, 'padding': 30, 'animate': True},
    'grid': {'name': 'grid', 'animate': True},
    'random': {'name': 'random', 'animate': True},
    'dagre': {'name': 'dagre', 'animate': True, 'rankDir': 'TB', 'nodeSep': 60, 'edgeSep': 100, 'rankSep': 100, 'ranker': 'network-simplex'},
    'breadthfirst': {'name': 'dagre', 'animate': True}
}

LAYOUT_LIST = [ 'cose', 'circle', 'concentric', 'grid', 'random', 'dagre', 'breadthfirst' ]

if __name__ == '__main__':
    pass
