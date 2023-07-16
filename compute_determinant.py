# //////////////////////////////////////////////////////////////////////////////
#  Copyright (c) 2023 Clemson University.
#
#  This file was originally written by Sayani Ghosh and Bradley S. Meyer.
#
#  This is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This software is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this software; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307
#  USA
#
# //////////////////////////////////////////////////////////////////////////////

import os
import glob
import argparse
from itertools import islice
import numpy as np
import networkx as nx

# Routine to create matrix digraph


def create_graph_from_matrix_file(file):

    G = nx.DiGraph()

    m = np.genfromtxt(file)

    a_diag = {}
    for i in range(m.shape[0]):
        if int(m[i, 0]) != int(m[i, 1]):
            if m[i, 2] != 0:
                G.add_edge(
                    int(m[i, 0]),
                    int(m[i, 1]),
                    weight=-m[i, 2],
                    lweight=np.log(np.abs(m[i, 2])),
                    sign=-np.sign(m[i, 2]),
                )
                if int(m[i, 1]) in a_diag:
                    a_diag[int(m[i, 1])] += m[i, 2]
                else:
                    a_diag[int(m[i, 1])] = m[i, 2]
        else:
            if int(m[i, 1]) in a_diag:
                a_diag[int(m[i, 1])] += m[i, 2]
            else:
                a_diag[int(m[i, 1])] = m[i, 2]

    for k in a_diag:
        if a_diag[k] != 0:
            G.add_edge(
                0,
                k,
                weight=a_diag[k],
                lweight=np.log(np.abs(a_diag[k])),
                sign=np.sign(a_diag[k]),
            )

    return G


def k_branchings(G, k, weight="lweight"):
    if k:
        return list(islice(nx.ArborescenceIterator(G, weight=weight, minimum=False), k))
    else:
        return list(nx.ArborescenceIterator(G, weight=weight, minimum=False))


parser = argparse.ArgumentParser(
    prog="branching_det",
    description="Compute a matrix determinant from branchings in the matrix digraph",
)

parser.add_argument("file", metavar="file", type=str, help="matrix text file")
parser.add_argument(
    "--k",
    metavar="k",
    type=int,
    help="maximum number of branchings to include (default is all branchings)",
)
parser.add_argument(
    "--output_dir",
    metavar="output_dir",
    type=str,
    help="output directory for branching graph pdfs)",
)
parser.add_argument(
    "--compare",
    metavar="compare",
    type=bool,
    default=False,
    help="compare determinant to that computed by LU decomposition",
)


args = parser.parse_args()

# Create graph

G = create_graph_from_matrix_file(args.file)

# Compute branchings and print out results

if args.output_dir:
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    else:
        files = glob.glob(args.output_dir + "/*")
        for f in files:
            os.remove(f)
else:
    print("Branchings\n")

i = 0
sum = 0
branchings = k_branchings(G, args.k)

for b in branchings:
    w = 1
    for u, v, d in b.edges(data=True):
        w *= d["weight"]
    sum += w
    if args.output_dir:
        A = nx.nx_agraph.to_agraph(G)
        A.edge_attr["color"] = "black"
        for u, v, d in G.edges(data=True):
            A.get_edge(u, v).attr["label"] = "{:.1f}".format(d["weight"])
        for u, v, d in b.edges(data=True):
            A.get_edge(u, v).attr["color"] = "red"
            A.get_edge(u, v).attr["fontcolor"] = "red"
        A.graph_attr["label"] = "Branching weight = {:.1f}".format(w)
        A.graph_attr["fontcolor"] = "red"
        A.layout(prog="dot")
        A.draw(args.output_dir + "/" + str(i) + ".pdf")
        i += 1
    else:
        print(b.edges, ": Weight = {:f}".format(w))

print("\nNumber of branchings = {:d}\n".format(len(branchings)))
print("\nDeterminant by branchings = {:f}\n".format(sum))

# Print out result computed from LU decomposition, if desired

if args.compare:
    N = len(G.nodes) - 1

    mat = np.zeros((N, N))

    m = np.genfromtxt(args.file)

    for k in range(m.shape[0]):
        mat[int(m[k, 0]) - 1][int(m[k, 1]) - 1] = m[k, 2]

    print("\nDeterminant by LU decomposition = {:f}\n".format(np.linalg.det(mat)))