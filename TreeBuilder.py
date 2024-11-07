import math
from SequenceData import Sequence

# for now treating elements of the matrix as if given (see 123A_F24_Deck07.pptx)

# STRATEGY:
#   1) compare all sequences against each other (list?), store abs minimum distance
#   2) use absolute minimum distance to find Nearest Neighbor (NN)
#   3) add NN to the list of sequences; calculate distances from NN to other seqs
#   4) remove the sequences that make NN from the list

# [A, B, C, D, E] => AB (A, B) => [A, B, C, D, E, (A, B)] => [C, D, E, (A, B)]
# => DE (D, E) => [C, D, E, (A, B), (D, E)] => [C, (A, B), (D, E)]
# => C,DE (C, (D, E)) => [C, (A, B), (D, E), (C, (D, E))] => [(A, B), (C, (D, E))]
# => ((A, B), (C, (D, E))) => [(A, B), (C, (D, E)), ((A, B), (C, (D, E)))]
# => ((A, B), (C, (D, E)))
# (though it should be in format ((A, B), ((D, E), C)))

class Tree:
    # In init, store tree as a list (newick format).
    #   https://en.wikipedia.org/wiki/Newick_format
    def __init__(self, seqList):
        self.tree = tuple() # initialize an empty tuple that will contain seq
        self.seqList = seqList

    # compare the distance between two sequences
    # return difference
    # TODO: Ask prof if we compare entire sequence or just until equal length
    def computeDistance(self, seq1, seq2):
        dif = 0
        for i in range(min(len(seq1), len(seq2))):
            if seq1[i] != seq2[i]:
                dif += 1
        return dif

    # here the main algorithm will occur
    def startWPGMA(self):
        NN = tuple()
        minDist = math.inf
        # compute distances between all sequences in self.seqList
        #   find minimum distance NN
        while len(self.seqList) > 1:
            # compare every element of seqList to all other elements, store min
            # create tuple with NN (eg (A, B)). Add to seqList
            # remove original seqs NN
            for i in range(len(self.seqList)):
                for j in range(len(self.seqList)):
                    if not self.seqList[i] == self.seqList[j]:
                        min(minDist, computeDistance(self.seqList[i], self.seqList[j]))
        self.tree = NN