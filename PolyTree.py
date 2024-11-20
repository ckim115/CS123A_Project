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
                    return False
    return True
#-----------------------------------------------------------------------
class WPGMA:
    def __init__(self, distance_matrix, labels):
        self.distance_matrix = np.array(distance_matrix)
        self.labels = labels
        self.tree = {}  # dict
        self.cur_tree = self.tree

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
        # find individual branch lengths for each node
        distance_x = distance_y = distance / 2

        # if a label has a preexisting length, we know its actual distance should be the difference
        #   between the label's distance and the given distance
        if self.labels[x] in self.tree:
            distance_x = distance_x - self.tree.get(self.labels[x])
        if self.labels[y] in self.tree:
            distance_y = distance_y - self.tree.get(self.labels[y])

        # in the label, put the individual distances
        new_label = f"({self.labels[x]}:{(distance_x):.2f},{self.labels[y]}:{(distance_y):.2f})"
        self.cur_tree = new_label
        self.tree[new_label] = distance / 2  # Store as half of the distance; this = total distance
        # Merge clusters and update labels
        self.labels = [lbl for i, lbl in enumerate(self.labels) if i != x and i != y] + [new_label]

    # Build the tree.
    def build_tree(self):
        while len(self.distance_matrix) > 1:
            x, y, min_dist = self.find_min_distance()
            self.merge_clusters(x, y, float(min_dist))
            self.update_distance_matrix(x, y)
        return self.cur_tree

    def print_tree(self):
        print("WPGMA Tree (Cluster, Distance):")
        for key, val in self.tree.items():
            print(f"{key} : {val:.2f}")
    
    def tree_info(self):
        tree_details = "WPGMA Tree (Cluster, Distance):\n"
        for key, val in self.tree.items():
            tree_details += f"{key} : {val:.2f}\n"
        return tree_details      
            
#----------------------------------------------------------------------------------
class NeighborJoining:
    def __init__(self, distance_matrix, labels):
        self.distance_matrix = np.array(distance_matrix, dtype=float)
        self.labels = labels[:]
        self.tree = []
    # biuld second matrix derived from the distance matrix ,named Q matrix
    # Q matrix is used to identify which nodes to merge
    def compute_q_matrix(self):
        n = len(self.distance_matrix)
        q_matrix = np.zeros((n, n))
        row_sums = np.sum(self.distance_matrix, axis=1)
        
        for i in range(n):
            for j in range(i + 1, n):
                q_matrix[i, j] = (n - 2) * self.distance_matrix[i, j] - row_sums[i] - row_sums[j]
                q_matrix[j, i] = q_matrix[i, j]
        return q_matrix
    # find lowest value in Q matrix
    def find_min_q(self, q_matrix):
        min_val = np.inf
        x, y = -1, -1
        for i in range(len(q_matrix)):
            for j in range(i + 1, len(q_matrix)):
                if q_matrix[i, j] < min_val:
                    min_val = q_matrix[i, j]
                    x, y = i, j
        return x, y

    def calculate_branch_lengths(self, i, j):
        n = len(self.distance_matrix)
        row_sums = np.sum(self.distance_matrix, axis=1)
        # Calculatethe branch lenghs 
        d_i = 0.5 * self.distance_matrix[i, j] + (row_sums[i] - row_sums[j]) / (2 * (n - 2))
        d_j = 0.5 * self.distance_matrix[i, j] + (row_sums[j] - row_sums[i]) / (2 * (n - 2))
        #Important part of algorithm
        # sometimes HJ generate negetive branch lenght in case of handeling a non-ultrametric distance matrix
        # one approch to fix it to make the negetive branch 0 and add same posetive amount to other branch
        if(d_i<0):
            d_j = d_j + abs(d_i)
            d_i=0
        if(d_j<0):
            d_i = d_i + abs(d_j)
            d_j=0    
        return round(d_i,3), round(d_j,3)
    
    # Update distance matric after merge two elements
    def update_distance_matrix(self, i, j, new_label):
        n = len(self.distance_matrix)
        new_row = []
        
        for k in range(n):
            if k != i and k != j:
                new_distance = 0.5 * (self.distance_matrix[i, k] + self.distance_matrix[j, k] - self.distance_matrix[i, j])
                new_row.append(new_distance)
                
        # Remove rows and columns of i and j
        self.distance_matrix = np.delete(self.distance_matrix, [i, j], axis=0)
        self.distance_matrix = np.delete(self.distance_matrix, [i, j], axis=1)
        
        new_matrix = np.zeros((self.distance_matrix.shape[0] + 1, self.distance_matrix.shape[1] + 1))
        # Copy the original matrix into the new matrix
        new_matrix[:self.distance_matrix.shape[0], :self.distance_matrix.shape[1]] = self.distance_matrix
        # Return the updated matrix with the new row and column set to zeros
        self.distance_matrix = new_matrix
        
        # Append new row and column
        new_row = np.array(new_row + [0])
        new_col = np.append(new_row[:-1], [0])
        
        self.distance_matrix[-1, :] = new_row
        self.distance_matrix[:, -1] = new_col    
        
        # Update labels
        self.labels = [label for idx, label in enumerate(self.labels) if idx != i and idx != j] + [new_label]
    
    def build_tree(self):
        while len(self.distance_matrix) > 2:
            q_matrix = self.compute_q_matrix()
            i, j = self.find_min_q(q_matrix)
            d_i, d_j = self.calculate_branch_lengths(i, j)
            new_label = f"({self.labels[i]}:{d_i}, {self.labels[j]}:{d_j})"
            self.tree.append(new_label)
            self.update_distance_matrix(i, j, new_label)
        # Handle the final two remaining labels
        final_dist = round(self.distance_matrix[0, 1],3)
        self.tree.append(f"({self.labels[0]}:{final_dist / 2}, {self.labels[1]}:{final_dist / 2})")
        return self.tree[-1]

    def print_tree(self):
        print("Neighbor-Joining Tree:")
        for node in self.tree:
            print(node)
            
    def tree_info(self):
        tree_details = "Neighbor-Joining Tree:\n"
        for node in self.tree:
            tree_details += f"{node}\n"
        return tree_details