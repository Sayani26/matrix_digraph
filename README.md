# siam_review_2023
Supplementary materials for the paper *Digraph Arborescences and Matrix Determinants*.  The python codes may require installation of the packages [numpy](https://numpy.org) and [networkx](https://networkx.org).  To create graph figures, install [pygraphviz](https://pygraphviz.github.io).

## Compute matrix determinants

The python code *compute_determinants.py* reads in a matrix, creates a matrix digraph, and computes the matrix determinant from the sum over arborescence weights.  To run the basic calculation, type

     python compute_determinant.py example_data/mat.txt

The code will print out the graph arborescences, their weights, and the sum (the determinant).  To compare to the determinant computed by LU decomposition, type

     python compute_determinant.py example_data/mat.txt --compare True

To create figures of the arborescences, type, for example,

     python compute_determinant.py example_data/mat2.txt --output_dir out

The output files are pdfs in the *out* directory.  They are labeled in decreasing order of the absolute value of the arborescence weight.

The files *example_data/mat3.txt* and *example_data/mat4.txt* provide examples of *reduced matrices*.  Use these data as example input for studying the rooted version of the *all minors theorem*.

## Create random matrices

One can of course use other matrices with the determinant code.  Copy one of the matrix files from *example_data* to the local directory, edit, and run the code.  Alternatively, run the *create_random_matrix.py* to create a file.  For example, type

    python create_random_matrix.py 3 > mat.txt

to create a 3 x 3 matrix.  The default largest absolute magnitude for an off-diagonal element is 1.  To change that, type

    python create_random_matrix.py 3 --x_max 5 > mat.txt

Use the matrix file created in this way with the matrix code:

    python compute_determinant.py mat.txt

For a large matrix, computation by a sum over arborescence weights will take a long time.  You can limit the sum to get an approximation.  For example, type

    python create_random_matrix.py 6 --x_max 2 > mat.txt
    
and then

    python compute_determinant.py mat.txt --compare True --k 1000

Increasing the number of terms in the sum (from, say, 1000 to 2000) better approximates the determinant but takes longer.  Note that, for a complete *N* vertex rooted digraph, there will be *(N+1)<sup>(N-1)</sup>* arborescences, so, for *N=6*, there will be 16,807 total arborescences.

## Factoring determinants

This code implements the factoring algorithm. To run this code have these scripts - factoring_code.py, numerical.py, label.py, rootify.py and matrix_graph.py in the same directory. To get started, type

     python factoring_code.py

The code will ask for a user input.

     Please enter numerical or label (default is numerical):

Choosing numerical will run the code on graph that has numerical edge weight and it will give a numerical value as determinant. Choosing 'label' will run the code on graph with string edge weights (a<sub>ij</sub>) and the determinant will be a string. 

If the choice is label, then the following is asked,

     Enter instruction in the format 'python label.py N --options True':

label.py is the script that performs the factoring algorithm on a graph with 'N'  vertices and string edge weights. To get PDFs of all the isolated branchings in a separate folder, type

     python label.py N --getpdfs True

If PDFs are not required as output simply omit '--getpdfs True' from the previous command. 

If the choice is numerical, the following is asked

     Enter instruction in the format 'python numerical.py example_data/filename.txt --options True':

numerical.py is the script that performs the factoring algorithm on a graph constructed from the matrix given as input. If you desire to use one of the matrices already in the example_data directory, type

        python numerical.py example_data/filename.txt --options True'

If you choose to use one of your own matrices, type

     python numerical.py filename.txt --options True'

The 'options' include comparing the determinant obtained from the factoring code with the determinant obtained by LU decomposition of the given matrix and to get PDFs of all the isolated branchings whose branching weights sum upto the determinant. To compare type '--compare' and to get PDFs type '--getpdfs' in place of '--options' in the previous command. To get nothing but the output omit '--options True' from the previous command.

    


