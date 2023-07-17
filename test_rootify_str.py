import networkx as nx
import copy
import rootify as rfy
import matplotlib.pyplot as plt

# A processing function--keeps track of cumulative weight and subgraph number


def my_func(G, data, num):
    p = " "
    for u, v, d in G.edges(data=True):
        # print('weight = ', d['label'])
        p += "("+d['label']+")"
    data[0] +=  "+" + p  
    # print('branching = ', data[0])
    num[0] += 1

# An add function--in fact identical to default

def my_add_func(G, root, u, v):
    if G.has_edge(root, v):
        G.get_edge_data(root, v)['label'] += '+'+G[u][v]['label']
    else:
        G.add_edge(root, v, label = G[u][v]['label'])

# Create graph

G = nx.DiGraph()

N = 3
for i in range(1, N+1):
    G.add_edge("root", str(i), weight=1, label = f'a{i}{i}')
    
for i in range(1, N+1):
    for j in range(1, N+1):
        if i != j:
            G.add_edge(str(i), str(j), weight=1, label = f'a{i}{j}')


# Print out graph

# for u, v, d in G.edges(data=True):
#     print(u, v, d['label'])


# Set functions

det =[""]
num = [0]
f = lambda G: my_func(G, det, num)

# Rootify

rfy.rootify(G, add_func=my_add_func, process_func=f)

# Print results:  det[0] will be sum of branching weights, num[0] will the
# the number of final rooted graphs (N! for complete graph)

print(det[0], num[0])
