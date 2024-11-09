class Sequence:
    # initialize sequence with scientific name and sequence
    def __init__(self, sci_name, sequence):
        self.sci_name = sci_name
        self.sequence = sequence

    # Return "scientific name: sequence"
    # TODO: change after testing to include sequence name
    def __str__(self):
        return f"{self.sci_name}"

    # T/F is this sequence equal to other sequence
    def __eq__(self, seq):
        return (self.sci_name == seq.sci_name) # and (self.sequence == seq.sequence)

    #Prints the scientific name and the sequence in a readable format.
    def print_sequence(self):
        print(f"Scientific Name: {self.sci_name}")
        print("Sequence: ".join(self.sequence))

    #Returns the sequence as a string.
    def get_sequence(self):
        return "".join(self.sequence)
    
    #Returns the length of the sequence.    
    def get_length(self):
        return len(self.sequence)


