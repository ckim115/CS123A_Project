from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk

import numpy as np
import pandas as pd

import PolyTree
import SeqAlignment
import TreeDisplay


class DashController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # use this list and pass to model to calculate the scores , create distance matrix and plot the tree
        # list is 2Xn dimention [name,sequence]
        self.seq_list = []
           
        self.plot_controller = None
        
        self.placeholder = "Enter sequences in following formats:\n\n1.Name and sequence seperately.\n\n2.FASTA formate: e.g.\n  >Name\n  Sequence\n"
        self.view.seq.insert(END, self.placeholder)
        self.view.seq.config(state="disable") 
         
        # Bind the Listbox click event to the view method
        self.view.select.bind("<<ListboxSelect>>", self.view_item)
        
        self.view.button_add.config(command=self.add_item)
        self.view.button_browse.config(command=self.browse_item)
        self.view.button_update.config(command=self.update_item)
        self.view.button_clear.config(command=self.clear_item)
        self.view.button_delete.config(command=self.delete_item)
        self.view.button_empty.config(command=self.clear_all_items)

        self.view.button_wpgma.config(command=lambda: self.plot_if_possible("WPGMA"))
        self.view.button_nj.config(command=lambda: self.plot_if_possible("Neighbor Joining"))
        # Bind events
        self.view.seq.bind("<FocusIn>", self.on_click)
        self.view.seq.bind("<FocusOut>", self.on_focus_out)
        
    def on_click(self,event=None):
        if self.view.seq.get("1.0", "end-1c") == self.placeholder:
            self.view.seq.config(state="normal")
            self.view.seq.delete("1.0", "end")
            self.view.seq.config(fg="black")
  
    def on_focus_out(self,event=None):
        if self.view.seq.get("1.0", "end-1c") == "":
            self.view.seq.insert("1.0", self.placeholder)
            self.view.seq.config(fg="gray")
            self.view.seq.config(state="disabled")
            
    # Method to clear all items from Listbox and datas list
    def clear_all_items(self,event=None):
        self.seq_list.clear()  # Clear the datas list
        self.view.select.delete(0, END)  # Clear all items in the Listbox    
               
    def add_item(self,event=None):
        # Retrieve values from entry and text widgets
        name_value = self.view.name.get().strip()
        seq_value = self.view.seq.get(1.0, "end-1c").strip()
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
        # Check if the sequence starts with '>' (Name included) or not (only sequence)
        if seq_value.startswith(">"):
            # Process the input sequence to extract name and sequence
            parsed_sequences = self.parse_sequences(seq_value)
            if parsed_sequences:
                for name_seq_pair in parsed_sequences:
                    self.seq_list.append(name_seq_pair)
                self.update_list(event=None)
                self.clear_item(event=None)  # Reset fields using the correct clear() function
            else:
                messagebox.showwarning("Input Error", "No valid sequences found in the input.")
        elif name_value == '':
            # If sequence is entered without a name (and not starting with '>'), show error
            messagebox.showwarning("Input Error", "Please provide input in FASTA format '>name' following by sequence on a new line or name and sequence seperately.")
                
        # Check if the sequence is valid
        elif not self.validate_sequence(seq_value):
            messagebox.showwarning("Invalid Sequence", 
                                  "Invalid input! Please follow this format:\n"
                                  "   1. FASTA format e.g.:\n"
                                  "      >Name\nSequence\n"
                                  "   2. Name and sequence seperatly without special characters or numbers.")
        else:
            # If both name and sequence are filled, add them to the list
            self.seq_list.append([name_value, seq_value])
            self.update_list(event=None)
            self.clear_item(event=None)
        return self.seq_list
       
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
    def browse_item(self,event=None):
        file_path = filedialog.askopenfilename(
        filetypes=[("Text and Fasta Files", "*.txt *.fasta"), ("Text Files", "*.txt"), ("Fasta Files", "*.fasta")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.view.seq.config(state="normal")
                    content = file.read().strip()
                    self.view.seq.config(fg="black")
                    self.view.seq.delete(1.0, "end")  # Clear the text area before inserting the content
                    self.view.seq.insert(1.0, content)  # Insert the content of the file
            except Exception as e:
                print(f"Error: {e}")
                messagebox.showerror("Error", f"Failed to load the file: {e}")

    # Update Listbox
    def update_list(self,event=None):
        # Clear the listbox
        self.view.select.delete(0, END)
        # Insert each name in list into the listbox
        for item in self.seq_list:
            self.view.select.insert(END, item[0])

    # View Information
    def view_item(self,event=None):
        selected_index = self.view.select.curselection()
        if selected_index:
            index = int(selected_index[0])
            # Enable the text widget
            self.view.seq.config(state="normal")
            # Clear and insert new text
            self.view.seq.delete(1.0, "end")
            self.view.seq.insert(1.0, self.seq_list[index][1])
            # Set text attributes and disable the widget
            self.view.seq.config(fg="black")
            # Update the entry field with the name
            self.view.name.set(self.seq_list[index][0])

    def update_item(self, event=None):
        selected_index = self.view.select.curselection()
        if selected_index:
            index = int(selected_index[0])
            # Get the new sequence from the text box
            new_seq = self.view.seq.get(1.0, "end-1c").strip()
            # Get the new name from the name entry widget
            new_name = self.view.name.get().strip()
            
            # Check if the sequence has changed
            if new_seq != self.seq_list[index][1]:
                # Update the sequence in the seq_list
                self.seq_list[index][1] = new_seq
                messagebox.showinfo("Sequence Updated", "The sequence has been updated successfully.")

            # Check if the name has changed
            if new_name != self.seq_list[index][0]:
                # Update the name in the seq_list
                self.seq_list[index][0] = new_name
                messagebox.showinfo("Name Updated", "The name has been updated successfully.")        
            self.update_list(event=None)

    # Delete Information
    def delete_item(self,event=None):
        selected_index = self.view.select.curselection()
        if selected_index:
            index = int(selected_index[0])
            del self.seq_list[index]
            self.update_list(event=None)
            self.clear_item(event=None)

    # Reset Fields
    def clear_item(self,event=None):
        self.view.name.set('')
        self.view.seq.delete(1.0, "end")
        self.on_focus_out(event=None)


    # Check if there are at least two sequences in datas
    def check_minimum_sequences(self):
        if len(self.seq_list) < 2:
            messagebox.showwarning("Insufficient Data", "Please enter at least two sequences to plot the tree.")
            return False
        return True
            
    def plot_if_possible(self,tree_type):
        if self.check_minimum_sequences():
            self.model.seq_list = self.seq_list
            self.plot_controller = PlotController(self.model,tree_type)
        return False               
            
class PlotController():
    def __init__(self,model,tree_type):
        self.model = model
        self.view = None  # Initialize view as None first
        from View import PlotView
        self.view = PlotView(model,tree_type)
        
        self.create_tree(tree_type)
    
    def create_tree(self, tree_type):
        df = pd.DataFrame(self.model.seq_list)
        labels = df[0].to_numpy()
        seqs = df[1].to_numpy()
        alignment = SeqAlignment.Score(seqs)
        # Compute pairwise distances
        matrix = alignment.compute_pairwise_distances()

        # Set the precision for printing NumPy arrays
        np.set_printoptions(precision=2)
        # Print the distance matrix
        alignment.print_distance_matrix(matrix)

        # Check if the matrix is ultrametric
        if PolyTree.test_ultrametricity(matrix):
            self.view.info_text.insert("end","Tree is ultrametric\n")
        else:
            self.view.info_text.insert("end","Tree is non ultrametric\n")
        if tree_type == "Neighbor Joining":
            tree = PolyTree.NeighborJoining(matrix, labels)
            tree.build_tree()
            tree.print_tree()
            self.view.info_text.insert("end", tree.tree_info())
        else:
            tree = PolyTree.WPGMA(matrix, labels)
            tree.build_tree()
            tree.print_tree()
            self.view.info_text.insert("end", tree.tree_info())
        
        
        print(self.view.info_text.get("1.0", "end-1c"))


        



    