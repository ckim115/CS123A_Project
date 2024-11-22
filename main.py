# main.py
from tkinter import Tk
from Model import AppModel
from View import *
from Controller import *

MAX_NAME_LENGTH = 100
MAX_SEQUENCE_LENGTH = 500000

if __name__ == "__main__":
    root = Tk()
    model = AppModel(MAX_NAME_LENGTH, MAX_SEQUENCE_LENGTH)
    view = DashView(root)
    controller = DashController(model, view)
    root.mainloop()