class Sequence:
    def __init__(self, sci_name, sequence):
        self.sci_name = sci_name
        self.sequence = sequence

    def __str__(self):
        return f"{self.sci_name}: {self.sequence}"