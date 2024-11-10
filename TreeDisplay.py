from Bio import Phylo
import matplotlib.pyplot as plt
from io import StringIO

class TreeDisplay:
    def __init__(self, labels, tree):
        self.labels = labels    # the labels for each sequence
        self.tree = tree

    def reformatTree(self):
        # here reformat from
        # ((A,B),(C,(D,E))) -> ((A:10.00,B:10.00):26.25,(C:22.50,(D:15.00,E:15.00):7.50):13.75)
        print(type(self.tree[0][0]))

    def visualize(self):
        # tree_data = self.reformatTree()
        # tree_data = "((A:10.00,B:10.00):26.25,(C:22.50,(D:15.00,E:15.00):7.50):13.75)"
        tree_data = "((A,B),(C,(D,E)))"
        tree_display = Phylo.read(StringIO(tree_data), "newick")
        print(tree_display)
        Phylo.draw(tree_display, branch_labels=lambda c: c.branch_length)
