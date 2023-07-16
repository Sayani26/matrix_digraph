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

import argparse
import numpy as np
import networkx as nx
import copy
import rootify as rfy
import matrix_graph as mg

# A processing function--keeps track of cumulative weight and subgraph number

def my_func(G, data, num):
    p = 1
    for u, v, d in G.edges(data=True):
        p *= d['weight']
    data[0] += p
    num[0] += 1

# An add function--in fact identical to default

def my_add_func(G, root, u, v):
    if G.has_edge(root, v):
        G.get_edge_data(root, v)['weight'] += G[u][v]['weight']
    else:
        G.add_edge(root, v, weight = G[u][v]['weight'])

parser = argparse.ArgumentParser(
    prog="branching_det",
    description="Factor a matrix determinant via the matrix digraph",
)

parser.add_argument("file", metavar="file", type=str, help="matrix text file")

parser.add_argument(
    "--compare",
    metavar="compare",
    type=bool,
    default=False,
    help="compare determinant to that computed by LU decomposition",
)

args = parser.parse_args()

# Create graph

G = mg.create_graph_from_matrix_file(args.file)

# Set functions

det =[0]
num = [0]
f = lambda G: my_func(G, det, num)

# Rootify

rfy.rootify(G, add_func=my_add_func, process_func=f)

# Print results:  det[0] will be sum of branching weights, num[0] will the
# the number of final rooted graphs (N! for complete graph)

print(det[0], num[0])

# Print out result computed from LU decomposition, if desired

if args.compare:
    print(
        "\nDeterminant by LU decomposition = {:f}\n".format(
            mg.compute_LU_determinant(G, args.file)
        )
    )
