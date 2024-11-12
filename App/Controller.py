from tkinter import *
from tkinter import messagebox
from tkinter import filedialog




class DashController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.datas = []
        self.plot_controller = None
        
        # Bind the Listbox click event to the view method
        self.view.select.bind("<<ListboxSelect>>", self.view_item)
        
        self.view.button_add.config(command=self.add_item)
        self.view.button_browse.config(command=self.browse_item)
        self.view.button_clear.config(command=self.clear_item)
        self.view.button_delete.config(command=self.delete_item)
        self.view.button_wpgma.config(command=lambda: self.plot_if_possible("WPGMA"))
        self.view.button_nj.config(command=lambda: self.plot_if_possible("Neighbor Joining"))
            
    def add_item(self):
        # Retrieve values from entry and text widgets
        name_value = self.view.name.get().strip().replace(":", "")
        seq_value = self.view.seq.get(1.0, "end-1c").strip().replace(":", "")
        
        # Check if the name or sequence exceeds the allowed length
        if len(name_value) > self.model.MAX_NAME_LENGTH:
            messagebox.showwarning("Name Length Exceeded", 
                                f"The name cannot be longer than {self.model.MAX_NAME_LENGTH} characters. "
                                f"Your input was {len(name_value)} characters long.")
            return
        
        if len(seq_value) > self.model.MAX_SEQUENCE_LENGTH:
            messagebox.showwarning("Sequence Length Exceeded", 
                                f"The sequence cannot be longer than {self.model.MAX_SEQUENCE_LENGTH} characters. "
                                f"Your input was {len(seq_value)} characters long.")
            return
        
        if  not seq_value:
            messagebox.showwarning("Sequence is empty", 
                                f"The sequence is not provided.")
            return

        # Check if the sequence is valid
        if not self.validate_sequence(seq_value):
            messagebox.showwarning("Invalid Sequence", 
                                "Invalid input! Sequences should only contain letters and follow the format:\n"
                                "1. '>name' followed by a sequence on the next line e.g., >name\nsequence\n"
                                "2. Just the sequence without special characters or numbers.")
            return

        # Check if the sequence starts with '>' (Name included) or not (only sequence)
        if seq_value.startswith(">"):
            # Process the input sequence to extract name and sequence
            parsed_sequences = self.parse_sequences(seq_value)
            if parsed_sequences:
                for name_seq_pair in parsed_sequences:
                    self.datas.append(name_seq_pair)
                self.update_list()
                self.clear_item()  # Reset fields using the correct clear() function
            else:
                messagebox.showwarning("Input Error", "No valid sequences found in the input.")
        elif name_value == '':
            # If sequence is entered without a name (and not starting with '>'), show error
            messagebox.showwarning("Input Error", "You must provide sequence in the format '>name' following by sequence on a new line or sequence with name seperately.")
        else:
            # If both name and sequence are filled, add them to the list
            self.datas.append([name_value, seq_value])
            self.update_list()
            self.clear_item()

    # Validate Sequence Format (Ensures only letters and newlines)
    def validate_sequence(self,seq_value):
        # Ensure the sequence contains only valid characters (letters, newlines, or '>')
        return all(c.isalpha() or c == '\n' or c == '>' or c==" "for c in seq_value)

    # Parse Sequences (Handles splitting multiple sequences)
    def parse_sequences(self,seq_value):
        sequences = []
        seq_lines = seq_value.splitlines()
        
        name = None
        sequence = None
        for line in seq_lines:
            line = line.strip()
            
            # If line starts with '>', it's a name line
            if line.startswith('>'):
                if name and sequence:  # If we already have a name and sequence, save them
                    sequences.append([name, sequence])
                name = line[1:].strip()  # Remove the '>' and store name
                sequence = ''  # Start a new sequence
            elif line:
                sequence += line  # Append the sequence part

        # Add the last sequence if available
        if name and sequence:
            # Remove all spaces from the last sequence and merge it as one
            sequence = ''.join(sequence.split())
            sequences.append([name, sequence])
        return sequences

    # Open File Dialog to Load .txt File
    def browse_item(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.read().strip()
                    self.view.seq.delete(1.0, "end")  # Clear the text area before inserting the content
                    self.view.seq.insert(1.0, content)  # Insert the content of the file
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the file: {e}")

    # Update Listbox
    def update_list(self):
        # Clear the listbox
        self.view.select.delete(0, END)
        # Insert each name in datas into the listbox
        for item in self.datas:
            self.view.select.insert(END, item[0])

    # View Information
    def view_item(self,event=None):
        selected_index = self.view.select.curselection()
        if selected_index:
            index = int(selected_index[0])
            self.view.name.set(self.datas[index][0])
            self.view.seq.delete(1.0, "end")
            self.view.seq.insert(1.0, self.datas[index][1])

    # Delete Information
    def delete_item(self):
        selected_index = self.view.select.curselection()
        if selected_index:
            index = int(selected_index[0])
            del self.datas[index]
            self.update_list()
            self.clear_item()

    # Reset Fields
    def clear_item(self):
        self.view.name.set('')
        self.view.seq.delete(1.0, "end")

    # Check if there are at least 2 sequences in datas
    def check_minimum_sequences(self):
        if len(self.datas) < 2:
            messagebox.showwarning("Insufficient Data", "Please enter at least 2 sequences to plot the tree.")
            return False
        return True
            
    def plot_if_possible(self,tree_type):
        if self.check_minimum_sequences():
            self.plot_controller = PlotController(self.view.root,self.model,tree_type)
        else:
            messagebox.showwarning("Insufficient Data", "Please enter at least 2 sequences to plot the tree.")  
        return FALSE                

class PlotController:
    def __init__(self,root, model,tree_type):
        self.model = model
        self.root = root
        from View import PlotView
        self.view = PlotView(root,self.model,tree_type)