import numpy as np
from PolyTree import WPGMA
import SeqAlignment
from TreeDisplay import TreeDisplay

# class Example
labels_1 = ["A", "B", "C", "D", "E"]
distance_matrix = [
    [0, 20, 60, 100, 90],
    [20, 0, 50, 90, 80],
    [60, 50, 0, 40, 50],
    [100, 90, 40, 0, 30],
    [90, 80, 50, 30, 0],
]

# Test WPGMA algorithm for class example
wpgma = WPGMA(distance_matrix, labels_1)
wpgma_tree = wpgma.build_tree()
wpgma.print_tree()

display = TreeDisplay(labels_1, wpgma_tree)
display.visualize()