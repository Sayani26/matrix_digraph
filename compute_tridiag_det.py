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
            abs(u - v) <= 1
        ), f"Arc ({u}, {v}) should not be in tridiagonal graph."

# Compute determinant recursively

d = G[0][1]["weight"]
d_tilde = 1

for i in range(1, G.number_of_nodes() - 1):
    dp = (G[i][i + 1]["weight"] + G[0][i + 1]["weight"]) * d + G[0][i + 1][
        "weight"
    ] * G[i + 1][i]["weight"] * d_tilde
    d_tilde = d + G[i + 1][i]["weight"] * d_tilde
    d = dp

print(f"\nDeterminant by recursion: {d:.{args.prec}f}")

# Compare to result computed from LU decomposition, if desired

if args.compare:
    print(
        f"\nDeterminant by LU decomposition = {mg.compute_LU_determinant_from_graph(G):.{args.prec}f}\n"
    )
