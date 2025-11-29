# //////////////////////////////////////////////////////////////////////////////
#  Copyright (c) 2023-2025 Clemson University.
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

# This code uses a depth-first search approach to isolating all vertices.

import networkx as nx
import copy
from itertools import combinations


def default_add_func(G, root, u, v):
    if G.has_edge(root, v):
        G.get_edge_data(root, v)["weight"] += G[u][v]["weight"]
    else:
        G.add_edge(root, v, weight=G[u][v]["weight"])


def sequential(G, add_func=None, process_func=None):

    #   Find the root

    root = [node for node in G.nodes if G.in_degree(node) == 0]

    if len(root) != 1:
        return

    #   Find non-isolated nodes

    v_r = [v for u, v in G.out_edges(root[0]) if G.out_degree[v] > 0]

    #   Process if no non-isolated nodes

    if len(v_r) == 0:
        if process_func:
            process_func(G)
        return

    #   Otherwise recurse

    else:
        processed_root_edges = []
        for r in v_r:
            G_c = copy.deepcopy(G)
            for e in processed_root_edges:
                G_c.remove_edge(*e)
            for e in [(u, v) for u, v in G.in_edges(r) if u != root[0]]:
                G_c.remove_edge(*e)
            for u, v in G.out_edges(r):
                if add_func:
                    add_func(G_c, root[0], u, v)
                else:
                    default_add_func(G_c, root[0], u, v)
                G_c.remove_edge(u, v)

            sequential(G_c, add_func=add_func, process_func=process_func)
            processed_root_edges.append((root[0], r))


def get_partitions(original_set):
    assert len(original_set) >= 2, "Set cannot be partitioned."

    partitions = []
    for i in range(1, len(original_set) // 2 + 1):
        for subset1_tuple in combinations(original_set, i):
            subset1 = set(subset1_tuple)
            subset2 = original_set - subset1

            if subset1 and subset2:
                partition_pair = tuple(
                    sorted((subset1, subset2), key=lambda x: sorted(list(x)))
                )
                if partition_pair not in partitions:
                    partitions.append(partition_pair)
    return partitions


def partitioned(G, add_func=None, process_func=None):

    #   Find the root

    root = [node for node in G.nodes if G.in_degree(node) == 0]

    if len(root) != 1:
        return

    #   Find non-isolated nodes

    s_r = {v for u, v in G.out_edges(root[0]) if G.out_degree[v] > 0}

    #   Process if no non-isolated nodes

    if len(s_r) == 0:
        if process_func:
            process_func(G)
        return

    #   Otherwise recurse

    else:
        s_r.add(root[0])
        for p in get_partitions(s_r):
            G_c = copy.deepcopy(G)
            s_rooted = p[0]
            s_not_rooted = p[1]
            if root[0] not in p[1]:
                s_not_rooted = p[0]
                s_rooted = p[1]
            for w in s_not_rooted:
                if w != root[0]:
                    G_c.remove_edge(root[0], w)
            for w in s_rooted:
                for e in [(u, v) for u, v in G.in_edges(w) if u != root[0]]:
                    G_c.remove_edge(*e)
            for w in s_rooted:
                for u, v in G.out_edges(w):
                    if G_c.has_edge(u, v):
                        if add_func:
                            add_func(G_c, root[0], u, v)
                        else:
                            default_add_func(G_c, root[0], u, v)
                        G_c.remove_edge(u, v)

            partitioned(G_c, add_func=add_func, process_func=process_func)
