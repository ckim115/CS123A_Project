from Bio import Phylo
from io import StringIO
import matplotlib.pyplot as plt

class TreeDisplay:
    def __init__(self, tree):
        self.tree = tree

    def visualize(self):
        tree_display = Phylo.read(StringIO(self.tree), "newick")
        print(tree_display)
        Phylo.draw(tree_display, branch_labels=lambda c: c.branch_length, do_show=False)
        plt.savefig('tree.png')
