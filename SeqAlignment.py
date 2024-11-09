import numpy as np

# This class calculates the optimal alignment score for some sequences using the Needleman-Wunsch algorithm.
class SequenceAlignment:
    def __init__(self, sequences, match_score=1, gap_penalty=-2, mismatch_penalty=-1):
        self.sequences = sequences
        self.match_score = match_score
        self.gap_penalty = gap_penalty
        self.mismatch_penalty = mismatch_penalty

    def needleman_wunsch(self, seq1, seq2):
        len1, len2 = len(seq1), len(seq2)
        score_matrix = np.zeros((len1 + 1, len2 + 1))

        # Initialize the scoring matrix with gap penalties
        for i in range(1, len1 + 1):
            score_matrix[i][0] = i * self.gap_penalty
        for j in range(1, len2 + 1):
            score_matrix[0][j] = j * self.gap_penalty

        # Fill in the score matrix
        for i in range(1, len1 + 1):
            for j in range(1, len2 + 1):
                match = score_matrix[i - 1][j - 1] + (self.match_score if seq1[i - 1] == seq2[j - 1] else self.mismatch_penalty)
                delete = score_matrix[i - 1][j] + self.gap_penalty
                insert = score_matrix[i][j - 1] + self.gap_penalty
                score_matrix[i][j] = max(match, delete, insert)

        return score_matrix[len1][len2]
    
    # This function calculates the optimal alignment score for two sequences using the Needleman-Wunsch algorithm.
    def compute_pairwise_distances(self):
        num_sequences = len(self.sequences)
        distance_matrix = np.zeros((num_sequences, num_sequences))

        # Calculate pairwise distances
        for i in range(num_sequences):
            for j in range(i + 1, num_sequences):
                alignment_score = self.needleman_wunsch(self.sequences[i], self.sequences[j])
                # This part of algorithm is . there are several ways to calculate distance.
                # Scaled Distance Formula used here. 0 means two sequent are very close
                # This formula asures that distance never get infinit or negetive value,always between 0 to 1
                distance = 1 / (1 + np.exp(alignment_score))
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        return distance_matrix
    
    # This function determine if a distance matrix of some sequences can form an ultrametric tree
    def is_ultrametric(self, distance_matrix):
        num_sequences = len(distance_matrix)

        # Check ultrametric condition for each triplet of sequences
        for i in range(num_sequences):
            for j in range(i + 1, num_sequences):
                for k in range(j + 1, num_sequences):
                    d_ij = distance_matrix[i][j]
                    d_ik = distance_matrix[i][k]
                    d_jk = distance_matrix[j][k]

                    # Check the ultrametric inequality
                    max_dist = max(d_ij, d_ik, d_jk)
                    if not ((d_ij == max_dist or d_ik == max_dist or d_jk == max_dist) and 
                            (d_ij <= max_dist and d_ik <= max_dist and d_jk <= max_dist)):
                        return "non ultrametric"
        return "ultrametric"

    def print_distance_matrix(self, distance_matrix):
        labels = [f"Seq{i+1}" for i in range(len(self.sequences))]
        print("Pairwise Distance Matrix:")
        print("      " + "  ".join(f"{label:>6}" for label in labels))
        for i, label in enumerate(labels):
            row = "  ".join(f"{distance_matrix[i][j]:6.2f}" for j in range(len(labels)))
            print(f"{label}  {row}")