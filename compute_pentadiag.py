# //////////////////////////////////////////////////////////////////////////////
#  Copyright (c) 2025 Clemson University.
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
import matrix_graph as mg

parser = argparse.ArgumentParser(
    prog="branching_det",
    description="Compute the determinant for a pentadiagonal matrix",
)

parser.add_argument(
    "--prec",
    metavar="prec",
    type=int,
    default=2,
    help="precision for output",
)

parser.add_argument(
    "--compare",
    action="store_true",
    help="compare determinant to that computed by LU decomposition",
)


parser.add_argument("file", metavar="file", type=str, help="matrix text file")

args = parser.parse_args()

# Create graph

G = mg.create_graph_from_matrix_file(args.file)

# Check that pentadiagonal

for u, v in G.edges():
    if u > 0:
        assert (
            abs(u - v) <= 2
        ), f"Arc ({u}, {v}) should not be in tridiagonal graph."

# Compute determinant recursively
#
# Notes:
#
#   det_n = current determinant
#   a_n = D_{(n)}
#   b_n = D_{(n-1)}
#   c_n = D_{(n-1, n)}
#   d_n = D_{(n)} with no path to n-1
#   e_n = D_{(n-1)} with no path to n
#
#   For the arcs, p refers to n+1, n to n, and m to n-1.

det_n = G[0][1]["weight"]
a_n = 1
b_n = 0
c_n = 0
d_n = 0
e_n = 0

for i in range(2, G.number_of_nodes()):
    v_pp = v_np = v_pn = v_pm = v_mp = 0
    if G.has_edge(0, i):
        v_pp = G[0][i]["weight"]
    if G.has_edge(i - 1, i):
        v_np = G[i - 1][i]["weight"]
    if G.has_edge(i, i - 1):
        v_pn = G[i][i - 1]["weight"]
    if i > 2:
        if G.has_edge(i, i - 2):
            v_pm = G[i][i - 2]["weight"]
        if G.has_edge(i - 2, i):
            v_mp = G[i - 2][i]["weight"]

    # Update values at n+1 based on values at n

    a_p = det_n + v_pn * a_n + v_pm * b_n + v_pn * v_pm * c_n
    b_p = a_n * (v_mp + v_np + v_pp) + v_pm * (v_np + v_pp) * c_n
    c_p = a_n + v_pm * c_n
    d_p = det_n + v_pm * e_n
    e_p = v_pp * a_n + v_mp * d_n + v_pp * v_pm * c_n

    det_p = (
        (v_mp + v_np + v_pp) * det_n
        + v_pp * v_pn * a_n
        + v_pp * v_pm * b_n
        + v_pp * v_pn * v_pm * c_n
        + v_pn * v_mp * d_n
        + v_pm * v_np * e_n
    )

    # Set updated to previous values for next iteration

    det_n = det_p

    a_n = a_p
    b_n = b_p
    c_n = c_p
    d_n = d_p
    e_n = e_p


print(f"\nDeterminant by recursion: {det_n:.{args.prec}f}")

# Compare to result computed from LU decomposition, if desired

if args.compare:
    print(
        f"\nDeterminant by LU decomposition = {mg.compute_LU_determinant_from_graph(G):.{args.prec}f}\n"
    )
