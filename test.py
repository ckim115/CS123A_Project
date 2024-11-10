import PolyTree2
from TreeDisplay import TreeDisplay
import PolyTree
import SeqAlignment
import numpy as np

# class Example
labels_1 = ["A", "B", "C", "D", "E"]
distance_matrix = [
    [0, 20, 60, 100, 90],
    [20, 0, 50, 90, 80],
    [60, 50, 0, 40, 50],
    [100, 90, 40, 0, 30],
    [90, 80, 50, 30, 0],
]

wpgma = PolyTree2.WPGMA2(distance_matrix, labels_1)
wpgma_tree = wpgma.build_tree()
wpgma.print_tree()

print(wpgma_tree)
display = TreeDisplay(labels_1, wpgma_tree)
display.visualize()

#--------------------------------------------
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
is_ultrametric = PolyTree2.test_ultrametricity(matrix_3)
print(str(is_ultrametric))
print()

# Run the WPGMA algorithm
wpgma2 = PolyTree2.WPGMA2(matrix_3, label_3)
wpgma_tree = wpgma2.build_tree()
wpgma2.print_tree()

print(wpgma_tree)
display = TreeDisplay(labels_1, wpgma_tree)
display.visualize()