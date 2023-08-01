import networkx as nx
import glob
import rootify as rfy
import matrix_graph as mg
import os.path
import argparse

def num_func(G, data, num, rooted_list):
    rooted_list.append(G)
    p = 1
    for u, v, d in G.edges(data=True):
        p *= d['weight']
    data[0] += p
    num[0] += 1

def label_func(G, v_det, num, rooted_list):
    rooted_list.append(G)
    p = ""
    i = 0
    for u, v, d in G.edges(data=True):
        p += "(" + d["label"] + ")"
    v_det.append(p)
    num[0] += 1


# An add function--in fact identical to default

def num_add_func(G, root, u, v):
    if G.has_edge(root, v):
        G.get_edge_data(root, v)['weight'] += G[u][v]['weight']
    else:
        G.add_edge(root, v, weight = G[u][v]['weight'])

def label_add_func(G, root, u, v):
    if G.has_edge(root, v):
        G.get_edge_data(root, v)["label"] += "+" + G[u][v]["label"]
    else:
        G.add_edge(root, v, label=G[u][v]["label"])


parser = argparse.ArgumentParser(
    prog="branching_det",
    description="Factor a matrix determinant via the matrix digraph",
)

parser.add_argument("file", metavar="file", type=str, help="matrix text file")

parser.add_argument(
    "--calc_type",
    metavar="calc_type",
    type=str,
    default="label",
    help="calculation type (\"numeric\" or \"label\", default=\"label\")"
)

parser.add_argument(
    "--output_dir",
    metavar="output_dir",
    type=str,
    help="output directory for pdf files of the fully rooted graphs",
)

args = parser.parse_args()

if args.output_dir:
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    else:
        files = glob.glob(args.output_dir + "/*")
        for f in files:
            os.remove(f)

# Create graph

G = mg.create_graph_from_matrix_file(args.file)

# Set functions

i = 0
num = [0]
rooted_list = []

if args.calc_type == "label":
    v_det = []
    f = lambda G: label_func(G, v_det, num, rooted_list)
    rfy.rootify(G, add_func=label_add_func, process_func=f)
    s_det = "\nDeterminant = " + "+".join(det for det in v_det)
elif args.calc_type == "numeric":
    det = [0]
    f = lambda G: num_func(G, det, num, rooted_list)
    rfy.rootify(G, add_func=num_add_func, process_func=f)
    s_det = "\nDeterminant = {:f}".format(det[0])
else:
    exit("{:s} is anncorrect calcution type".format(args.calc_type))

print(s_det + "\n")

# Make pdfs

if args.output_dir:
    i = 0

    for g in rooted_list:
        A = nx.nx_agraph.to_agraph(g)
        A.edge_attr["color"] = "black"

        if args.calc_type == "label":
            v_w = []
            for u, v, d in g.edges(data=True):
                A.get_edge(u, v).attr["label"] = d["label"]
                v_w.append("(" + d["label"] + ")")
            s_w = "".join(w for w in v_w)
        else:
            w = 1
            for u, v, d in g.edges(data=True):
                A.get_edge(u, v).attr["label"] = "{:.1f}".format(d["weight"])
                w *= d["weight"]
            s_w = "{:f}".format(w)

        A.graph_attr["label"] = "Branching weight = " + s_w
        A.graph_attr["fontcolor"] = "black"
        A.layout(prog="dot")
        A.draw(args.output_dir + "/out_" + str(i) + ".pdf")
        i += 1