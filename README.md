# matrix_digraph

This repository contains python codes to explore the connection between matrix determinants and directed graphs, as embodied in the matrix-tree and matrix-forest theorems and described in the paper *Digraph Arborescences and Matrix Determinants* by S. Ghosh and B. S. Meyer.  The python codes may require installation of the packages [numpy](https://numpy.org) and [networkx](https://networkx.org).  To create graph figures, install [pygraphviz](https://pygraphviz.github.io).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.666173055.svg)](https://doi.org/10.5281/zenodo.10268261)


## Preliminaries

The python codes in this repository work with $n \times n$ matrix matrices.  Such matrices are denoted $A = \left[a_{ij}\right]$.
The matrix elements $a_{ij}$ of $A$ are taken to be


$$
a_{ij} = 
\begin{cases}
-v_{ij}, & i\ne j, 1 \leq i, j \leq n\\
 \sum_{k = 1} v_{kj}, & i = j, 1 \leq i \leq n
\end{cases}
$$

The sum of the elements in column $j$ of the matrix $A$ is thus $v_{jj}$.  The matrix is converted to a directed graph (digraph) such that, for each $i \ne j$, there is an arc from vertex $i$ to vertex $j$ with weight $v_{ij}$.  In addition, the graph includes a "root" vertex $0$ such there is an arc from vertex $0$ to vertex $j$ with weight $v_{jj}$.  The codes construct the matrix digraph from the matrix and compute determinants from the matrix-tree and matrix-forest theorems, as described in the parent paper.

## Compute matrix determinants

The python code *compute_determinants.py* reads in a matrix, creates a matrix digraph, and computes the matrix determinant from the sum over arborescence weights.  To run the basic calculation, type

     python compute_determinant.py example_data/mat.txt

The code will print out the graph arborescences, their weights, and the sum (the determinant).  To compare to the determinant computed by LU decomposition, type

     python compute_determinant.py example_data/mat.txt --compare

To create figures of the arborescences, type, for example,

     python compute_determinant.py example_data/mat2.txt --output_dir out

The output files are pdfs in the *out* directory.  They are labeled in decreasing order of the absolute value of the arborescence weight.  To change the precision of the output, use the *prec* option.  For example, to change from the default two decimal places to five, type

     python compute_determinant.py example_data/mat2.txt --output_dir out --prec 5

The files *example_data/mat3.txt* and *example_data/mat4.txt* provide examples of *reduced matrices*.  Use these data as example input for studying the rooted version of the *all minors theorem*.

## Create random matrices

One can of course use other matrices with the determinant code.  Copy one of the matrix files from *example_data* to the local directory, edit, and run the code.  Alternatively, run the *create_random_matrix.py* to create a file.  For example, type

    python create_random_matrix.py 3 > mat.txt

to create a 3 x 3 matrix.  The default largest absolute magnitude for an off-diagonal element is 1.  To change that, type

    python create_random_matrix.py 3 --x_max 5 > mat.txt

One may also set the sum of each column of the matrix to a fixed value with the *fixed_col_sum* option.  For example, type

    python create_random_matrix.py 3 --fixed_col_sum 1 > mat.txt

Use the matrix file created in this way with the matrix code:

    python compute_determinant.py mat.txt

For a large matrix, computation by a sum over arborescence weights will take a long time.  You can limit the sum to get an approximation.  For example, type

    python create_random_matrix.py 6 --x_max 2 > mat.txt
    
and then

    python compute_determinant.py mat.txt --compare --k 1000

Increasing the number of terms in the sum (from, say, 1000 to 2000) better approximates the determinant but takes longer.  Note that, for a complete *N* vertex rooted digraph, there will be *(N+1)<sup>(N-1)</sup>* arborescences, so, for *N=6*, there will be 16,807 total arborescences.

## Tridiagonal matrices

The code *compute_tridiag_det.py* implements the tridiagonal matrix determinant recursive approach described in *Digraph Arborescences and Matrix Determinants* by S. Ghosh and B. S. Meyer.  To run the basic calculation, type

     python compute_tridiag_det.py example_data/trid.txt --prec 4

To compare the result to that from LU decomposition, add the keyword argument *compare*:

     python compute_tridiag_det.py example_data/trid.txt --prec 4 --compare

To compute a random tridiagonal matrix, use the *create_random_matrix.py* code but add the *tridiag* keyword argument:

     python create_random_matrix.py 6 --x_max 2 --tridiag > trid.txt

This matrix can then be used with the tridiagonal matrix determinant code:

     python compute_tridiag_det.py trid.txt --prec 6 --compare
     

## Factoring determinants

The code *factor_determinant.py* implements the vertex-isolating approach in the paper *On Directed Graphs with the Same Sum over
Arborescence Weights* by S. Ghosh and B. S. Meyer.  The output determinant is either a numerical value or a sum of products of arc weight labels.  The default calculation is for arc weight labels.  To run the basic calculation, type

     python factor_determinant.py example_data/mat.txt

The output shows the determinant value for the input matrix in terms of arc labels, as computed by the factorization/isolation procedure described in the paper.  To instead compute the numerical value of the determinant, type

     python factor_determinant.py example_data/mat.txt --calc_type numeric

To output the individual fully isolated (rooted) graphs for the matrix, type

     python factor_determinant.py example_data/mat.txt --output_dir out_label --calc_type label

The output pdfs will be in the directory *out_label*.  Note that, in this case, the *--calc_type label* option is not necessary since the label calculation is the default.  To produce the individual numerical graphs, type

     python factor_determinant.py example_data/mat.txt --output_dir out_numeric --calc_type numeric

Again, the pdfs will be in the *out_numeric* directory.  It is, of course, possible to use other input matrices, for example, use *example_data/mat2.txt* or a matrix computed with the *compute_random_matrix.py* code as input.  For numerical calculations, the output precision can be set with the *prec* option.  For example, type

     python factor_determinant.py example_data/mat.txt --output_dir out_numeric --calc_type numeric --prec 6

to change from the default precision 2 to 6.

