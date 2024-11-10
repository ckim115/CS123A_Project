# IN MAIN:
#   take in a input txt file. make Sequence objects using the sequences
# inputted in the file. Then pass this list of sequences to Tree
import numpy as np
import PolyTree
import SeqAlignment

#---------------------------------------------------   
# class Example - ultrametric 
labels_1 = ["A", "B", "C", "D","E"]
distance_matrix = [
    [0,   20, 60,  100,90],
    [20,  0,  50,  90, 80],
    [60,  50, 0,   40, 50],
    [100, 90, 40,  0,  30],
    [90, 80,  50,  30,  0],
]
# Check if the matrix is ultrametric
is_ultrametric = PolyTree.test_ultrametricity(distance_matrix)
print(str(is_ultrametric))
print()

# Test WPGMA algorithm for class example
wpgma = PolyTree.WPGMA(distance_matrix, labels_1)
wpgma_tree = wpgma.build_tree()
wpgma.print_tree()
#----------------------------------------------------
 # new example - non ultrametric:
label_3 = ["s1","s2","s3","s4","s5","s6"]
sequences_3 = [
    "ATGCATGC",    # Sequence 1
    "ATGCAACG",    # Sequence 2
    "TTCCGCCC",    # Sequence 3
    "GCCGGTGA",    # Sequence 4
    "CCCT C A",    # Sequence 5 
    "CCC GTGA"     # Sequence 6
]

alignment = SeqAlignment.Score(sequences_3)
# Compute pairwise distances
matrix_3 = alignment.compute_pairwise_distances()

# Set the precision for printing NumPy arrays
np.set_printoptions(precision=2)
# Print the distance matrix
alignment.print_distance_matrix(matrix_3)
print()

# Check if the matrix is ultrametric
is_ultrametric = PolyTree.test_ultrametricity(matrix_3)
print(str(is_ultrametric))
print()

# Run the WPGMA algorithm
wpgma2 = PolyTree.WPGMA(matrix_3, label_3)
wpgma_tree = wpgma2.build_tree()
wpgma2.print_tree()

# For now just getting general thoughts on the project direction

# WPGMA/UPGMA
# Pairwise alignment of all pairs of input seqs
# Compute evolutionary distance between all pairs
# Make distance table
# While table size > 1x1
    # Choose pair of “nearest neighbors” (we decide what that means)
    # Cluster them
    # Recompute slightly smaller distance table (‘how’ depends on WPGMA/UPGMA)

# Prior to this program: we want to have already done PWA and computed pairwise distances
# 2D array
# Algorithm as example in Deck07.pptx
    # Multiple clusters (while table size > 1x1...)
    # We want to traverse array to find nearest neighbor
    # add each cluster to table and compute distance
    # remove the original portions of the cluster from the table
    # so on so forth

# How we can partition the work?
    # One of us works on traversal (fxn for finding the smallest nearest neighbor)

    # Another works on computing distance between new clusters

    # Then one of us works on removing original portions from the table (ex if we get
    #   {AB} then we remove A and B from row/col

    # After that we also need to consider getting user input to put into the table, but
    #   for now we can work with pre-set values from the slides because trying user inputs
    #   while implementing the WGMA algorithm will just make things confusing
    # But it shouldnt take too long on its own, so whoever did only 1 of the above tasks
    #   can take this one