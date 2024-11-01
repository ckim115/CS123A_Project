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

