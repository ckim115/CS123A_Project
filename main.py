# IN MAIN:
#   take in a input txt file. make Sequence objects using the sequences
# inputted in the file. Then pass this list of sequences to Tree
from SequenceData import Sequence
from TreeBuilder import Tree

def main():
    a = Sequence('A', '')
    b = Sequence('B', '')
    c = Sequence('C', '')
    d = Sequence('D', '')
    e = Sequence('E', '')
    test_tree = Tree([a, b, c, d, e])
    print("Starting WPGMA")
    test_tree.startWPGMA()
    print(test_tree)

if __name__=="__main__":
    main()


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