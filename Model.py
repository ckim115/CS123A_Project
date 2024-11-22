# models/model.py

class AppModel:
    def __init__(self, max_name_length, max_sequence_length):
        self.seq_list = []
        self.MAX_NAME_LENGTH = max_name_length
        self.MAX_SEQUENCE_LENGTH = max_sequence_length
        self.img_path = "tree.png"


