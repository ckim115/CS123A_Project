# models/model.py
from tkinter import messagebox

class AppModel:
    def __init__(self, max_name_length, max_sequence_length):
        self.MAX_NAME_LENGTH = max_name_length
        self.MAX_SEQUENCE_LENGTH = max_sequence_length
        # use this list and pass to model to calculate the scores , create distance matrix and plot the tree
        # list is 2Xn dimention [name,sequence]
        self.seq_list = []
        #use this variables to do calculation and make a tree, you can pass the tree as png to gui
        #use info varibale to send everything we generate as text about the tree in this format:
        #   name of tree:
        #   number of seq:
        #   Tree type: ultrametric or not
        #   text format of tree:
        self.info = "Info from model class:\nName of tree:\nIs ultrametric or not?\nPrint the tree in string form\nHow many sequences was used to make the tree, etc.\nTo copy info: (Ctrl+C)."
        #here I use path of png file but you can change it to png file or any object type you like and pass it to view.py
        #then in Plotview class plot the image, I put comment on the section that plot the tree to make it easier to undreastand
        self.img_path = "example.png"
        

