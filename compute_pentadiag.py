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
    description="Compute the determinant for a tridiagonal matrix",
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

# Check that tridiagonal

for u, v in G.edges():
    if u > 0:
        assert (
            abs(u - v) <= 2
        ), f"Arc ({u}, {v}) should not be in tridiagonal graph."

# Compute determinant recursively

det = G[0][1]["weight"]
a = 1
b = 0
c = 0
d = 0
e = 0

for i in range(2, G.number_of_nodes()):
    v_pp = G[0][i]["weight"]
    v_np = G[i - 1][i]["weight"]
    v_pn = G[i][i - 1]["weight"]
    v_pm = 0
    v_mp = 0
    if i > 2:
        v_pm = G[i][i - 2]["weight"]
        v_mp = G[i - 2][i]["weight"]

    a_n = det + v_pn * a + v_pm * b + v_pn * v_pm * c
    b_n = a * (v_mp + v_np + v_pp) + v_pm * (v_np + v_pp) * c
    c_n = a + v_pm * c
    d_n = det + v_pm * e
    e_n = v_pp * a + v_mp * d + v_pp * v_pm * c

    det = (
        (v_mp + v_np + v_pp) * det
        + v_pp * v_pn * a
        + v_pp * v_pm * b
        + v_pp * v_pn * v_pm * c
        + v_pn * v_mp * d
        + v_pm * v_np * e
    )
    a = a_n
    b = b_n
    c = c_n
    d = d_n
    e = e_n


print(f"\nDeterminant by recursion: {det:.{args.prec}f}")

# Compare to result computed from LU decomposition, if desired

if args.compare:
    print(
        f"\nDeterminant by LU decomposition = {mg.compute_LU_determinant_from_graph(G):.{args.prec}f}\n"
    )
