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
    # TODO: check if seq1/seq2 is a tuple, in which case we must calc inside first
    # return difference
    # FOR INITIAL TESTING: JUST HARDCODE
    # TODO: Ask prof if we compare entire sequence or just until equal length
    
    def computeDistance(self, seq1, seq2):
        print("\tComputing distance between:", seq1, seq2)
        # check for tuple
        if type(seq1) is tuple and type(seq2) is tuple:
            return ((Tree.computeDistance(self, seq1[0], seq1[1]) + Tree.computeDistance(self, seq2[0], seq2[1]))/2)
        if type(seq2) is tuple:
            return ((Tree.computeDistance(self, seq1, seq2[0]) + Tree.computeDistance(self, seq1, seq2[1]))/2)
        if type(seq1) is tuple:
            return ((Tree.computeDistance(self, seq1[0], seq2) + Tree.computeDistance(self, seq1[1], seq2))/2)
        if seq1.sci_name == 'A':
            if seq2.sci_name == 'B':
                return 20
            if seq2.sci_name == 'C':
                return 60
            if seq2.sci_name == 'D':
                return 100
            if seq2.sci_name == 'E':
                return 90
        if seq1.sci_name == 'B':
            if seq2.sci_name == 'A':
                return 20
            if seq2.sci_name == 'C':
                return 50
            if seq2.sci_name == 'D':
                return 90
            if seq2.sci_name == 'E':
                return 80
        if seq1.sci_name == 'C':
            if seq2.sci_name == 'A':
                return 60
            if seq2.sci_name == 'B':
                return 50
            if seq2.sci_name == 'D':
                return 40
            if seq2.sci_name == 'E':
                return 50
        if seq1.sci_name == 'D':
            if seq2.sci_name == 'A':
                return 100
            if seq2.sci_name == 'B':
                return 90
            if seq2.sci_name == 'C':
                return 40
            if seq2.sci_name == 'E':
                return 30
        if seq1.sci_name == 'E':
            if seq2.sci_name == 'A':
                return 90
            if seq2.sci_name == 'B':
                return 80
            if seq2.sci_name == 'C':
                return 50
            if seq2.sci_name == 'D':
                return 30

        # BELOW: only for testing after initial hardcoded testing
        # dif = 0
        # for i in range(min(len(seq1), len(seq2))):
        #     if seq1[i] != seq2[i]:
        #         dif += 1
        # return dif

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
                seq1 = self.seqList[i] # first sequence element
                for j in range(i+1, len(self.seqList)):
                    seq2 = self.seqList[j] # second sequence elmement
                    if not i == j:
                        d = Tree.computeDistance(self, seq1, seq2)
                        print("\t\tDistance:", d)
                        if minDist > d:
                            minDist = d
                            NN = (seq1, seq2)
                            print("Current nearest neighbor:", NN[0], NN[1], "at dist", d)

            # remove original elements
            print("Final neighbors:", NN[0], NN[1])
            self.seqList.remove(NN[0])
            self.seqList.remove(NN[1])
            # push new sequence pair onto list of sequences
            print("Adding NN to list")
            self.seqList.append(NN)
            minDist = math.inf # reset minDist

        self.tree = NN

    def getStr(self, tree):
        inner = ""
        if type(tree) is tuple:
            inner += Tree.getStr(self, tree[0]) + ", "+ Tree.getStr(self, tree[1])
        else:
            return str(tree)
        return ("(" + inner + ")")

    def __str__(self):
        return Tree.getStr(self, self.tree)
