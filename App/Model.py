# models/model.py
from tkinter import messagebox

class AppModel:
    def __init__(self, max_name_length, max_sequence_length):
        self.seq_list = []
        self.info = "Info from model class:\nName of tree:\nIs ultrametric or not?\nPrint the tree in string form\nHow many sequences was used to make the tree, etc.\nTo copy info: (Ctrl+C)."
        self.img_path = "example.png"
        self.MAX_NAME_LENGTH = max_name_length
        self.MAX_SEQUENCE_LENGTH = max_sequence_length

