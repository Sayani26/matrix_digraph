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

args = parser.parse_args()

A = np.zeros((args.N, args.N))

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        if i == j:
            A[i, j] += args.x_max * rng.random()
        else:
            aij = args.x_max * rng.random()
            A[i, j] -= aij
            A[j, j] += aij

for i in range(A.shape[0]):
    for j in range(A.shape[1]):
        print(i + 1, j + 1, A[i, j]) 
           
