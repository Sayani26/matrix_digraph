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
                    label="v{:d}{:d}".format(int(m[i, 0]), int(m[i, 1])),
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
                label="v{:d}{:d}".format(k, k),
            )

    return G

# Routine to compute matrix determinant by LU decomposition

def compute_LU_determinant(file):

    m = np.genfromtxt(file)

    N = max(
        np.hstack((np.asarray(m[:, 0], dtype="int"), np.asarray(m[:, 1], dtype="int")))
    )

    mat = np.zeros((N, N))

    for k in range(m.shape[0]):
        mat[int(m[k, 0]) - 1][int(m[k, 1]) - 1] = m[k, 2]

    return np.linalg.det(mat)
