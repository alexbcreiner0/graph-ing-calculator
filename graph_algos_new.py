from graph import Graph

def get_adj_list_from_edges(edges, keys, weights= None):
    adj_list = {}
    for (u,v) in edges:
        if u not in adj_list:
            if weights: 
                adj_list[u] = {v: weights[edges.index((u,v))]}
            else: 
                adj_list[u] = [v]
        else:
            if weights:
                adj_list[u][v] = weights[edges.index((u,v))]
            else:
                adj_list[u].append(v)
    for key in keys:
        if key not in adj_list:
            if weights:
                adj_list[key] = {}
            else:
                adj_list[key] = []
    return adj_list

def depth_first_traverse_undirected(G, is_weighted):
    def explore(u, visited, clock, pre, post, G, hist= None, pred= None):
        if hist == None: hist = []
        visited[u] = True
        pre[u] = clock
        clock += 1
        if pred: hist.append((pred,u))
        for nbr in G[u]:
            if not visited[nbr]:
                clock, hist = explore(u= nbr, visited= visited, clock= clock, pre= pre, post= post, G= G, hist= hist, pred= u)
        post[u] = clock
        clock += 1
        return clock, hist

    if len(G) == 0: return G

    H = []
    visited = {v: False for v in G}
    clock = 1
    pre = {v: None for v in G}
    post = {v: None for v in G}

    for u in G:
        if not visited[u]:
            clock, tree = explore(u, visited, clock, pre, post, G)
            H += tree

    all_edges = Graph(G, digraph= False, weighted= is_weighted).edges
    for (u,v) in list(H): H.append((v,u))
    
    fake_extra_edges = list(set(all_edges).difference(set(H)))
    extra_edges = []
    for (u,v) in fake_extra_edges:
        if (v,u) not in extra_edges:
            extra_edges.append((u,v))

    new_H = []
    new_edges = []
    new_extra_edges = []
    weights = []
    all_weights = []
    for (u,v) in all_edges:
        new_u, new_v = str(u)+': '+str(pre[u])+', '+str(post[u]), str(v)+': '+str(pre[v])+', '+str(post[v])
        new_edges.append((new_u,new_v))
        if is_weighted: all_weights.append(G[u][v])
        if (u,v) in H:
            new_H.append((new_u, new_v))
            if is_weighted: weights.append(G[u][v])
        if (u,v) in extra_edges: new_extra_edges.append((new_u, new_v))
        
    new_pre, new_post = {}, {}
    for u in G:
        new_u = str(u)+': '+str(pre[u])+', '+str(post[u])
        new_pre[new_u] = pre[u]
        new_post[new_u] = post[u]

    if len(weights) > 0:
        new_adj_list_colors = get_adj_list_from_edges(new_edges, list(new_pre.keys()), all_weights)
    else:
        new_adj_list_colors = get_adj_list_from_edges(new_edges, list(new_pre.keys()))
    if len(weights) > 0:
        new_adj_list = get_adj_list_from_edges(new_H, list(new_pre.keys()), weights)
    else:
        new_adj_list = get_adj_list_from_edges(new_H, list(new_pre.keys()))

    output_vanilla = Graph(new_adj_list, digraph= False, weighted= is_weighted, layout= 'dagre')
    output_extra = Graph(new_adj_list_colors, digraph= False, weighted= is_weighted, layout= 'dagre')
    for (u,v) in new_extra_edges:
        if new_pre[v] < new_pre[u] and new_post[u] < new_post[v]:
            output_extra.color_edge((u,v), 'back')
        elif new_pre[u] < new_pre[v] and new_post[v] < new_post[u]:
            output_extra.color_edge((u,v), 'forward')
        else:
            output_extra.color_edge((u,v), 'cross') 
    return output_vanilla, output_extra

def depth_first_traverse(G, display_extra_edges= False, is_directed= True, is_weighted= False):
    if is_directed:
        G, G_extra = depth_first_traverse_directed(G, is_weighted)
        return G, G_extra
    else:
        G, G_extra = depth_first_traverse_undirected(G, is_weighted)
        return G, G_extra
    

def depth_first_traverse_directed(G, is_weighted): # G assumed to be an adjacency list
    def explore(u, visited, clock, pre, post, G, hist= None, pred= None):
        if hist == None: hist = []
        visited[u] = True
        pre[u] = clock
        clock += 1
        if pred: hist.append((pred, u))
        for nbr in G[u]:
            if not visited[nbr]:
                clock, hist = explore(u=nbr, visited= visited, clock= clock, pre= pre, post= post, G= G, hist= hist, pred= u)
        post[u] = clock
        clock += 1
        return clock, hist
    
    if len(G) == 0: return G

    H = [] # Set of edges traversed in the DFS
    visited = {v: False for v in G}
    clock = 1
    pre = {v: None for v in G}
    post = {v: None for v in G}

    for u in G:
        if not visited[u]:
            clock, tree = explore(u, visited, clock, pre, post, G)
            H += tree

    weights = []
    all_weights = []
    all_edges = []
    new_H = []

    for u in G:
        for v in G[u]:
            new_u, new_v = str(u)+': '+str(pre[u])+', '+str(post[u]), str(v)+': '+str(pre[v])+', '+str(post[v])
            all_edges.append((new_u, new_v))
            if is_weighted: all_weights.append(G[u][v])
            if (u,v) in H:
                new_H.append((new_u, new_v))
                if is_weighted: weights.append(G[u][v])

    new_pre, new_post = {}, {}
    for u in G:
        new_u = str(u)+': '+str(pre[u])+', '+str(post[u])
        new_pre[new_u] = pre[u]
        new_post[new_u] = post[u]

    if len(weights) > 0:
        new_adj_list_colors = get_adj_list_from_edges(all_edges, list(new_pre.keys()), all_weights)
    else:
        new_adj_list_colors = get_adj_list_from_edges(all_edges, list(new_pre.keys()))
    if len(weights) > 0:
        new_adj_list = get_adj_list_from_edges(new_H, list(new_pre.keys()), weights)
    else:
        new_adj_list = get_adj_list_from_edges(new_H, list(new_pre.keys()))

    output_vanilla = Graph(new_adj_list, digraph= True, weighted= is_weighted, layout= 'dagre')
    output_extra = Graph(new_adj_list_colors, digraph= True, weighted= is_weighted, layout= 'dagre')       

    extra_edges = list(set(all_edges).difference(set(new_H)))
    for (u,v) in extra_edges:
        if new_pre[v] < new_pre[u] and new_post[u] < new_post[v]:
            output_extra.color_edge((u,v), 'back')
        elif new_pre[u] < new_pre[v] and new_post[v] < new_post[u]:
            output_extra.color_edge((u,v), 'forward')
        else:
            output_extra.color_edge((u,v), 'cross') 

    return output_vanilla, output_extra

if __name__ == "__main__":
    edges = [('A', 'B'), ('A', 'C'), ('B', 'E'), ('E', 'F'), ('E', 'H'), ('F', 'G'), ('C', 'D')]
    weights = [5, 12, 3, -2, 6, 8, 24]
    print(get_adj_list_from_edges(edges, weights))
