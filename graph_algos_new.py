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

def replace_names(old_names_list, new_names_list):
    pass

def depth_first_traverse(G, display_extra_edges= False): # G assumed to be an adjacency list
    def explore(u, visited, clock, pre, post, G, hist= None, pred= None):
        print(f"Exploring {u}, pred is {pred}")
        if hist == None: hist = []
        visited[u] = True
        pre[u] = clock
        clock += 1
        if pred: hist.append((pred, u))
        for nbr in G[u]:
            print(f"Looking at neighbor {nbr}")
            if not visited[nbr]:
                print(f"{nbr} not yet visited. calling explore with pred= {pred}")
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
            print(f"Finished exploring {u}, tree of visits is {tree}")
            H += tree

    print(f"H is {H}")
    print(f"Pres are: {pre}")
    print(f"Posts are: {post}")

    weights = []
    all_weights = []
    all_edges = []
    new_H = []

    for u in G:
        for v in G[u]:
            new_u, new_v = str(u)+': '+str(pre[u])+', '+str(post[u]), str(v)+': '+str(pre[v])+', '+str(post[v])
            all_edges.append((new_u, new_v))
            if type(G[u]) == dict:
                all_weights.append(G[u][v])
            if (u,v) in H:
                new_H.append((new_u, new_v))
                if type(G[u]) == dict:
                    weights.append(G[u][v])

    new_pre, new_post = {}, {}
    for u in G:
        new_u = str(u)+': '+str(pre[u])+', '+str(post[u])
        new_pre[new_u] = pre[u]
        new_post[new_u] = post[u]

    if display_extra_edges:
        if len(weights) > 0:
            new_adj_list = get_adj_list_from_edges(all_edges, list(new_pre.keys()), all_weights)
        else:
            new_adj_list = get_adj_list_from_edges(all_edges, list(new_pre.keys()))
    else:
        if len(weights) > 0:
            new_adj_list = get_adj_list_from_edges(new_H, list(new_pre.keys()), weights)
        else:
            new_adj_list = get_adj_list_from_edges(new_H, list(new_pre.keys()))

    output = Graph(new_adj_list, digraph= True)
        
    if display_extra_edges:
        extra_edges = list(set(all_edges).difference(set(new_H)))
        for (u,v) in extra_edges:
            if new_pre[v] < new_pre[u] and new_post[u] < new_post[v]:
                output.color_edge((u,v), 'back')
            elif new_pre[u] < new_pre[v] and new_post[v] < new_post[u]:
                output.color_edge((u,v), 'forward')
            else:
                output.color_edge((u,v), 'cross') 
    return output

if __name__ == "__main__":
    edges = [('A', 'B'), ('A', 'C'), ('B', 'E'), ('E', 'F'), ('E', 'H'), ('F', 'G'), ('C', 'D')]
    weights = [5, 12, 3, -2, 6, 8, 24]
    print(get_adj_list_from_edges(edges, weights))
