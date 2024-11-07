class Sequence:
    # initialize sequence with scientific name and sequence
    def __init__(self, sci_name, sequence):
        self.sci_name = sci_name
        self.sequence = sequence

    # T/F is this sequence equal to other sequence
    def __eq__(self, seq):
        return (self.sci_name == seq.sci_name) && (self.sequence == seq.sequence)

    # Return "scientific name: sequence"
    def __str__(self):
        return f"{self.sci_name}: {self.sequence}"