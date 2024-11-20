from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from matplotlib import figure

class DashView:
    def __init__(self, root):
        self.root = root
        self.root.title("Phylogenetic Tree Plotter")
        self.root.geometry('600x450')
        self.root.minsize(600, 450)
        self.root.maxsize(600, 450)
        self.datas = []
        
        # Frames
        self.frame_top = Frame(root)
        self.frame_top.pack(side="top", fill="both", expand=False,pady=10)
        
        self.frame_center = Frame(root)
        self.frame_center.pack(side="top", fill="both", expand=False)
        
        self.frame_left = Frame(self.frame_center)
        self.frame_left.pack(side="left", fill="x", expand=True, pady=10, padx=10)
        
        self.frame_right = Frame(self.frame_center)
        self.frame_right.pack(side="right", fill="both", expand=True, pady=10, padx=10)
        
        self.frame_option = Frame(root)
        self.frame_option.pack(side="top", fill="none", expand=False, padx=20)
        
        self.frame_bottom = Frame(root)
        self.frame_bottom.pack(side="top", fill="x", expand=False, pady=30,padx=20)

        # GUI Components
        self.title = Label(self.frame_top, text='Phylogenetic Tree Plotter', font='arial 20 bold')
        self.title.pack(side=TOP, anchor="center")

        # Entry Fields
        self.name = StringVar()
        self.txt = StringVar()
        
        Label(self.frame_left, text='Name:', font='arial 12 bold', anchor="w").pack(side=TOP, fill="x", padx=20, anchor="w")
        self.name_entry = Entry(self.frame_left, textvariable=self.name, width=50)
        self.name_entry.pack(side=TOP, fill="x", padx=20, pady=5)
        
        Label(self.frame_left, text='Sequence(s):', font='arial 12 bold', anchor="w").pack(side=TOP, fill="x", padx=20, anchor="w")
        self.scroll_text = Scrollbar(self.frame_left, orient=VERTICAL, width=20)  # Set scrollbar width
        self.seq = Text(self.frame_left,fg="gray", wrap=WORD, width=37, height=10)
        self.scroll_text.config(command=self.seq.yview)
        self.scroll_text.pack(side=RIGHT, fill=Y)
        self.seq.pack(side=TOP, fill="x", padx=20, pady=5)
        
        # Buttons
        self.button_add = Button(self.frame_option, text="Add", font="arial 12 bold", width=6)
        self.button_add.pack(side=LEFT, padx=8)
              
        self.button_browse = Button(self.frame_option, text="Browse", font="arial 12 bold", width=6)
        self.button_browse.pack(side=LEFT, padx=8)  
        
        self.button_update = Button(self.frame_option, text="Update", font="arial 12 bold", width=6)
        self.button_update.pack(side=LEFT, padx=8)
        
        self.button_clear = Button(self.frame_option, text="Clear", font="arial 12 bold", width=6)
        self.button_clear.pack(side=LEFT, padx=8)

        self.button_delete = Button(self.frame_option, text="Delete", font="arial 12 bold",width=6)
        self.button_delete.pack(side=LEFT, padx=8)
        
        self.button_empty = Button(self.frame_option, text="Empty", font="arial 12 bold",width=6)
        self.button_empty.pack(side=LEFT, padx=8)
        
        # Create a Listbox 
        Label(self.frame_right, text='List:', font='arial 12 bold', anchor="w").pack(side=TOP, fill="y", padx=10, anchor="w")
        self.scroll_bar = Scrollbar(self.frame_right, orient=VERTICAL, width=20) 
        self.select = Listbox(self.frame_right, yscrollcommand=self.scroll_bar.set, height=12)
        self.scroll_bar.config(command=self.select.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y) 
        self.select.pack(side=LEFT, fill="both", padx=0, pady=0)  


        # Create both buttons in frame_bottom with commands to open PlotView
        self.button_wpgma = Button(self.frame_bottom, text="WPGMA", font="arial 12 bold", width=12)
        self.button_wpgma.pack(side=LEFT, padx=5, fill="both", expand=True)

        self.button_nj = Button(self.frame_bottom, text="Neighbor Joining", font="arial 12 bold", width=12)
        self.button_nj.pack(side=LEFT, padx=5, fill="both", expand=True)

        
class PlotView:
    def __init__(self, model, tree_type):
        self.model = model
        # Create a new window
        self.plot_window = Toplevel(None)
        self.plot_window.title(f"{tree_type} Tree Plot")
        self.plot_window.geometry("600x550")
        self.plot_window.minsize(600, 575)
        self.plot_window.resizable(True, True)
        
        # Top frame for plot display title
        self.frame_top = Frame(self.plot_window, padx=5, pady=5)
        self.frame_top.pack(side="top", fill="x")
        
        # Title Label in the top frame
        self.plot_label = Label(self.frame_top, text=f"{tree_type} Plot", font="arial 12", anchor="center")
        self.plot_label.pack(side="top",fill="x", expand=True)
        
        # Middle frame for displaying the plot
        self.frame_middle = Frame(self.plot_window, padx=5, pady=5)
        self.frame_middle.pack(side="top", fill="both", expand=True)
        
###-------------------------------------------------------------------------------------------------
###Here is the part help to plot the image of tree, use bio lab to make an image then pass it here
        # Save Plotly figure to an image file
        #Load and display the image (replace with the actual path of the image)
        
        img_path = "tree.png"
        newImg = showImg(self.frame_middle)
        newImg.update_image(img_path)
        
###-------------------------------------------------------------------------------------------------
       
        # # Bottom frame for information display
        self.frame_bottom = Frame(self.plot_window,padx=10, pady=10)
        self.frame_bottom.pack(side="top", fill="both", expand=True)
        
        # Text box for showing information
        self.scroll_info = Scrollbar(self.frame_bottom, orient=VERTICAL, width=20) 
        self.info_text = Text(self.frame_bottom, wrap=WORD)
        self.scroll_info.config(command=self.info_text.yview)
        self.scroll_info.pack(side=LEFT, fill=Y) 
        self.info_text.pack(fill="both", expand=True)

class showImg:
    def __init__(self, frame_middle):
        self.frame_middle = frame_middle
        self.image_label = None  # Keep reference to the label

    def update_image(self, img_path):
        # Open and resize the new image
        img = Image.open(img_path)
        img = img.resize((600, 400), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)

        # Create a new label with the updated image
        self.image_label = Label(self.frame_middle, image=img_tk)
        self.image_label.image = img_tk  # Keep reference to prevent garbage collection
        self.image_label.pack(fill="both", expand=True)
