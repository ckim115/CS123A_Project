import io
import numpy as np
from Bio import Align
# This class calculates the optimal alignment score for some sequences using the Needleman-Wunsch algorithm.
class Score:
    def __init__(self, sequences, match_score=0.001, gap_penalty=-0.002, mismatch_penalty=-0.001):
        self.sequences = sequences
        self.aligner = Align.PairwiseAligner() # aligner for two sequences
        
        self.aligner.match_score = match_score
        self.aligner.mismatch_score = mismatch_penalty
        self.aligner.open_gap_score = gap_penalty
        self.aligner.extend_gap_score = gap_penalty
        self.aligner.target_end_gap_score = 0.0
        self.aligner.query_end_gap_score = 0.0

    
    # This function calculates the optimal alignment score for two sequences using the Needleman-Wunsch algorithm.
    def compute_pairwise_distances(self):
        print("beginning pairwise alignment")
        num_sequences = len(self.sequences)
        distance_matrix = np.zeros((num_sequences, num_sequences))
        # (t,n,p variable) This part is informative and only shows
        # % progress of calculation. t is total numbel of alignment
        # n is number of alignment done and p is the percent of pregress.
        t = 0.5*num_sequences*(num_sequences-1)
        n = 0
        # Calculate pairwise distances
        for i in range(num_sequences):
            for j in range(i + 1, num_sequences):
                
                n += 1  # Increment progress counter
                p = (n / t) * 100  # Calculate percentage
                print(f"Progress: {p:.2f}%")
                
                score = self.aligner.score(self.sequences[i], self.sequences[j])
    
                # This part of algorithm is important. there are several ways to calculate distance.
                # Scaled Distance Formula used here. 0 means two sequent are very close vast versa
                # This formula assures that distance never get infinit or negetive value,always between 0 to 1
                # Handle score = 0 to avoid log(0) and devision by 0
                if score == 0:
                    #the alignment score is zero, which could be due to no similarity between two sequences.
                    distance = 1.0  # Maximum distance for no similarity
                else:
                    max_value = np.log(score) - 1
                    score = np.clip(score, -max_value, max_value)
                    distance = 1 / (1 + np.exp(score))
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance

        return distance_matrix
    
    def print_distance_matrix(self, distance_matrix):
        # Create a memory buffer to capture the output
        output_buffer = io.StringIO()
        labels = [f"Seq{i+1}" for i in range(len(self.sequences))]
        # Capture the pairwise distance matrix header and rows into the buffer
        output_buffer.write("Pairwise Distance Matrix:\n")
        output_buffer.write("      " + "  ".join(f"{label:>6}" for label in labels) + "\n")
        for i, label in enumerate(labels):
            row = "  ".join(f"{distance_matrix[i][j]:6.2f}" for j in range(len(labels)))
            output_buffer.write(f"{label}  {row}\n")
        return output_buffer.getvalue()
    
            