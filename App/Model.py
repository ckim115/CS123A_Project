# models/model.py
from tkinter import messagebox

class AppModel:
    def __init__(self, max_name_length, max_sequence_length):
        self.datas = []
        self.MAX_NAME_LENGTH = max_name_length
        self.MAX_SEQUENCE_LENGTH = max_sequence_length

