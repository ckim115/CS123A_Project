from tkinter import *

class DashView:
    def __init__(self, root):
        self.root = root
        self.root.title("Phylogenetic Tree Plotter")
        self.root.geometry('500x500')
        self.root.minsize(600, 500)

        self.datas = []
        
        # Frames
        self.frame_top = Frame(root)
        self.frame_top.pack(side="top", fill="both", expand=False)
        
        self.frame_center = Frame(root)
        self.frame_center.pack(side="top", fill="both", expand=False)
        
        self.frame_left = Frame(self.frame_center)
        self.frame_left.pack(side="left", fill="x", expand=True, pady=10, padx=10)
        
        self.frame_right = Frame(self.frame_center)
        self.frame_right.pack(side="right", fill="both", expand=True, pady=10, padx=10)
        
        self.frame_option = Frame(root)
        self.frame_option.pack(side="top", fill="none", expand=False, padx=20)
        
        self.frame_bottom = Frame(root)
        self.frame_bottom.pack(side="top", fill="x", expand=True, padx=20)

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
        self.seq = Text(self.frame_left, width=37, height=10)
        self.seq.pack(side=TOP, fill="x", padx=20, pady=5)
        
        # Buttons
        self.button_add = Button(self.frame_option, text="Add", font="arial 12 bold", width=8)
        self.button_add.pack(side=LEFT, padx=10)
              
        self.button_browse = Button(self.frame_option, text="Browse", font="arial 12 bold", width=8)
        self.button_browse.pack(side=LEFT, padx=10)  
        
        self.button_clear = Button(self.frame_option, text="Clear", font="arial 12 bold", width=8)
        self.button_clear.pack(side=LEFT, padx=10)
        
        self.button_delete = Button(self.frame_option, text="Delete", font="arial 12 bold",width=8)
        self.button_delete.pack(side=LEFT, padx=10)
        
        
        # Create a Listbox 
        Label(self.frame_right, text='List:', font='arial 12 bold', anchor="w").pack(side=TOP, fill="x", padx=10, anchor="w")
        self.scroll_bar = Scrollbar(self.frame_right, orient=VERTICAL, width=20) 
        self.select = Listbox(self.frame_right, yscrollcommand=self.scroll_bar.set, height=12)
        self.scroll_bar.config(command=self.select.yview)
        self.scroll_bar.pack(side=RIGHT, fill=Y) 
        self.select.pack(side=LEFT, fill="both", padx=0, pady=0)  


        # Create both buttons in frame_bottom with commands to open PlotView
        self.button_wpgma = Button(self.frame_bottom, text="WPGMA", font="arial 12 bold")
        self.button_wpgma.pack(side=LEFT, padx=5, fill="both", expand=True)

        self.button_nj = Button(self.frame_bottom, text="Neighbor Joining", font="arial 12 bold")
        self.button_nj.pack(side=LEFT, padx=5, fill="both", expand=True)

        
class PlotView:
    def __init__(self, root,model, tree_type):
        # Create a new window
        self.plot_window = Toplevel(root)
        self.plot_window.title(f"{tree_type} Tree Plot")
        self.plot_window.geometry("400x500")
        self.plot_window.minsize(450, 600)
        self.plot_window.resizable(True, True)
        
        # Top frame for plot display title
        self.frame_top = Frame(self.plot_window, width=100, height=50, padx=10, pady=10)
        self.frame_top.pack(side="top", fill="x")
        
        # Title Label in the top frame
        self.plot_label = Label(self.frame_top, text=f"{tree_type} Plot", font="arial 14", anchor="center")
        self.plot_label.pack(fill="both", expand=True)
        
        # Middle frame for displaying the PNG image
        self.frame_middle = Frame(self.plot_window, width=400, height=400, padx=10, pady=10)
        self.frame_middle.pack(side="top", fill="both", expand=True)
        
        self.plot_label = Label(self.frame_middle, text="Plot", font="arial 14", anchor="center")
        self.plot_label.pack(fill="both", expand=True)
        # Load and display the image
        # try:
        #     img = Image.open("img.png")  # Replace with actual image path
        #     img = img.resize((500, 240), Image.ANTIALIAS)
        #     img_tk = ImageTk.PhotoImage(img)
            
        #     image_label = Label(self.frame_middle, image=img_tk)
        #     image_label.image = img_tk  # Keep reference to prevent garbage collection
        #     image_label.pack(fill="both", expand=True)
        # except Exception as e:
        #     messagebox.showerror("Image Error", f"Could not load image: {e}")
        
        # Bottom frame for information display
        self.frame_bottom = Frame(self.plot_window, width=100, height=50, padx=10, pady=10)
        self.frame_bottom.pack(side="top", fill="both", expand=True)
        
        # Text box for showing information
        self.info_text = Text(self.frame_bottom, wrap=WORD)
        self.info_text.pack(fill="both", expand=False)
        self.info_text.insert(END, f"Information about {tree_type} tree goes here.")