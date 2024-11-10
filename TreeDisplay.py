from Bio import Phylo
import matplotlib.pyplot as plt
from io import StringIO

class TreeDisplay:
    def __init__(self, labels, tree):
        self.labels = labels    # the labels for each sequence
        self.tree = tree

    def visualize(self):
        # tree_data = "((A:10.00,B:10.00):26.25,(C:22.50,(D:15.00,E:15.00):7.50):13.75)"
        tree_display = Phylo.read(StringIO(self.tree), "newick")
        print(tree_display)
        Phylo.draw(tree_display, branch_labels=lambda c: c.branch_length)
