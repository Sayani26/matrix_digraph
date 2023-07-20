import networkx as nx
import copy
import rootify as rfy
import matplotlib.pyplot as plt
import os.path


# A processing function--keeps track of cumulative weight and subgraph number
def my_func(G, data, num, rooted_list):
    rooted_list.append(G)
    p = " "
    i = 0
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
i = 0
det =[""]
num = [0]
rooted_list = []
f = lambda G: my_func(G, det, num, rooted_list)

# Rootify

rfy.rootify(G, add_func=my_add_func, process_func=f)

# Print results:  det[0] will be sum of branching weights, num[0] will the
# the number of final rooted graphs (N! for complete graph)

print(det[0], num[0])

# create pdfs of rooted graphs
i = 0
current_directory = os.getcwd()
final_directory = os.path.join(current_directory, r'out_rooted')
if not os.path.exists(final_directory):
   os.makedirs(final_directory)

output_path = 'out_rooted/'
for g in rooted_list:
    A = nx.nx_agraph.to_agraph(g)
    A.edge_attr["color"] = "black"
    w  = " "
    for u, v, d in g.edges(data=True):
        A.get_edge(u, v).attr["label"] = "("+d['label']+")" #" ".format(d['label'])
        w += "("+d['label']+")"
    A.graph_attr["label"] = "Branching weight = " + w
    A.graph_attr["fontcolor"] = "black"
    A.layout(prog="dot")
    A.draw(output_path + 'out_' + str(i) + '.pdf')
    i += 1
