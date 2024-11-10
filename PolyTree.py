import numpy as np


# The function to check if a matrix is ultrametric
def test_ultrametricity(distance_matrix):
    num_sequences = len(distance_matrix)

    # Check ultrametric condition for each triplet of sequences
    for i in range(num_sequences):
        for j in range(i + 1, num_sequences):
            for k in range(j + 1, num_sequences):
                # Get the distances for the triplet
                d_ij = distance_matrix[i][j]
                d_ik = distance_matrix[i][k]
                d_jk = distance_matrix[j][k]
                
                # Check the ultrametric inequality: 
                # The maximum distance should occur at least twice
                if not ((d_ij <= (d_ik+d_jk)) and 
                        (d_ik <= (d_ij+d_jk)) and 
                        (d_jk <= (d_ij+d_ik))):
                    return "Tree is non ultrametric"
    return "tree is ultrametric"

class WPGMA:
    def __init__(self, distance_matrix, labels):
        self.distance_matrix = np.array(distance_matrix)
        self.labels = labels
        self.tree = []
    
    # Find the pair of clusters with the smallest distance
    def find_min_distance(self):
        min_dist = np.inf
        x, y = -1, -1
        for i in range(len(self.distance_matrix)):
            for j in range(i + 1, len(self.distance_matrix)):
                if self.distance_matrix[i][j] < min_dist:
                    min_dist = self.distance_matrix[i][j]
                    x, y = i, j
        return x, y, min_dist

    # Update the distance matrix after merging two clusters
    def update_distance_matrix(self, x, y):
        # Create a new row by averaging the distances of two clusters to others
        new_row = [(self.distance_matrix[x][i] + self.distance_matrix[y][i]) / 2
                   for i in range(len(self.distance_matrix)) if i != x and i != y]
        
        # Create the new matrix excluding the rows and columns of x and y
        new_matrix = []
        for i in range(len(self.distance_matrix)):
            if i != x and i != y:
                new_row_i = [self.distance_matrix[i][j] for j in range(len(self.distance_matrix)) if j != x and j != y]
                new_matrix.append(new_row_i)

        # Append the new row and column for the merged cluster
        new_matrix.append(new_row + [0])
        for i in range(len(new_row)):
            new_matrix[i].append(new_row[i])
        
        # Update the distance matrix
        self.distance_matrix = np.array(new_matrix)

    # Merge two clusters and update the tree.
    def merge_clusters(self, x, y, distance):
        new_label = f"({self.labels[x]},{self.labels[y]})"
        self.tree.append((new_label, distance / 2))  # Store as half of the distance
        # Merge clusters and update labels
        self.labels = [lbl for i, lbl in enumerate(self.labels) if i != x and i != y] + [new_label]
    
    # Build the tree.
    def build_tree(self):
        while len(self.distance_matrix) > 1:
            x, y, min_dist = self.find_min_distance()
            self.merge_clusters(x, y, float(min_dist))
            self.update_distance_matrix(x, y)
        return self.tree
        
    def print_tree(self):
        print("WPGMA Tree (Cluster, Distance):")
        for node in self.tree:
            print(f"{node[0]} : {node[1]:.2f}")
