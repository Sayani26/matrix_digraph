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

import argparse
import numpy as np

rng = np.random.default_rng()

parser = argparse.ArgumentParser(
    prog="create_random_matrix",
    description="Create a random matrix with negative off-diagonal elements and a non-zero column sum",
)

parser.add_argument(
    "N",
    metavar="N",
    type=int,
    help="Number of rows/columns in matrix",
)

parser.add_argument(
    "--x_max",
    metavar="x_max",
    type=float,
    default=1,
    help="maximum absolute value of off-diagonal element",
)

parser.add_argument(
    "--fixed_col_sum",
    metavar="fixed_col_sum",
    type=float,
    default=None,
    help="fixed value for each column (default: not set)",
)

parser.add_argument(
    "--tridiag",
    action="store_true",
    help="tridiagonal matrix",
)

args = parser.parse_args()

A = np.zeros((args.N, args.N))

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        if i == j:
            if args.fixed_col_sum:
                A[i, j] += args.fixed_col_sum
            else:
                A[i, j] += args.x_max * rng.random()
        else:
            if (args.tridiag and abs(i - j) <= 1) or not args.tridiag:
                aij = args.x_max * rng.random()
                A[i, j] -= aij
                A[j, j] += aij

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        if A[i, j]:
            print(i + 1, j + 1, A[i, j])
