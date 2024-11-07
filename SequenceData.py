class Sequence:
    # initialize sequence with scientific name and sequence
    def __init__(self, sci_name, sequence):
        self.sci_name = sci_name
        self.sequence = sequence

    # Return "scientific name: sequence"
    # TODO: change after testing to include sequence name
    def __str__(self):
        return f"{self.sci_name}"

    # T/F is this sequence equal to input
    def __eq__(self, seq):
        return type(seq) is Sequence and (self.sci_name == seq.sci_name) # and (self.sequence == seq.sequence)

    # T/F is this sequence not equal to input
    def __ne__(self, seq):
        if not type(seq) is Sequence:
            return True
        if self.sci_name == seq.sci_name: # and (self.sequence == seq.sequence)
            return True
        return False
