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

import networkx as nx
import copy


def default_add_func(G, root, u, v):
    if G.has_edge(root, v):
        G.get_edge_data(root, v)["weight"] += G[u][v]["weight"]
    else:
        G.add_edge(root, v, weight=G[u][v]["weight"])


def rootify(G, add_func=None, process_func=None):

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

            rootify(G_c, add_func=add_func, process_func=process_func)
            processed_root_edges.append((root[0], r))


def y_rootify(
    G,
    start_vertex,
    add_func=None,
    process_func=None,
    marked_property="marked",
    marked_value="yes",
):

    #  Find the root

    root = [node for node in G.nodes if G.in_degree(node) == 0]

    if len(root) != 1:
        print("Graph not properly rooted.")
        exit()

    #  Make a copy of the graph, find the rooted vertex, mark, and remove in arcs

    G_c = copy.deepcopy(G)

    for e in [(u, v) for u, v in G.in_edges(start_vertex) if u != root[0]]:
        G_c.remove_edge(*e)

    G_c[root[0]][start_vertex][marked_property] = marked_value

    #  Call the rootifier

    _y_rootify(G_c, add_func, process_func, marked_property, marked_value)


def _y_rootify(
    G,
    add_func=None,
    process_func=None,
    marked_property="marked",
    marked_value="yes",
):

    #   Find the root

    root = [node for node in G.nodes if G.in_degree(node) == 0]

    if len(root) != 1:
        print("Graph not properly rooted.")
        exit()

    #   Find non-isolated marked nodes

    v_r = [
        v
        for u, v, a in G.out_edges(root[0], data=True)
        if G.out_degree[v] > 0 and marked_property in a
    ]

    #   Rootify if no non-isolated marked nodes

    if len(v_r) == 0:
        rootify(G, add_func=add_func, process_func=process_func)
        return

    #   Otherwise recurse

    else:
        processed_edges = []
        for r in v_r:
            for u, v, a in G.out_edges(r, data=True):
                G_c = copy.deepcopy(G)
                for e in processed_edges:
                    G_c.remove_edge(*e)
                for e in [(u, w) for (u, w) in G_c.in_edges(v)]:
                    G_c.remove_edge(*e)
                G_c.add_edge(root[0], v)
                for p in a:
                    G_c[root[0]][v][p] = a[p]
                G_c[root[0]][v]["marked"] = "yes"
                _y_rootify(G_c, add_func, process_func, marked_property, marked_value)
                processed_edges.append((u, v))

        G_c = copy.deepcopy(G)
        marked_nodes = [
            v for u, v, a in G.out_edges(root[0], data=True) if marked_property in a
        ]
        for v in marked_nodes:
            for e in G.out_edges(v):
                G_c.remove_edge(*e)

        rootify(G_c, add_func=add_func, process_func=process_func)
