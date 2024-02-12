import customtkinter as ctk
from customtkinter import *
import tkinter as tk
from tkinter import ttk


class Base(ctk.CTkFrame):
    def __init__(self, *args, header_name="Add Damages", **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ["A", "B", "C", "D", "E"]
        self.second_options = ["1", "2", "3", "4", "5"]

        self.selections = {}
        self.is_option_selected = False
        self.main_func()

    def main_func(self):
        
        self.box_var = ctk.StringVar()
        self.box_option = ctk.CTkComboBox(self, values=self.options, variable=self.box_var)
        self.box_option.grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 20), padx=10)
        self.box_var2 = ctk.StringVar()
        box_option2 = ctk.CTkComboBox(self, values=self.second_options, variable=self.box_var2)
        box_option2.grid(row=0, column=2, columnspan=2, sticky='w', pady=(10, 20), padx=10)


        self.display_box = ctk.CTkFrame(self, height=500, width=300)
        self.display_box.grid(row=0, column=4, sticky='w', pady=(10, 20), padx=10)

        #self.selected_options = ctk.CTkTextbox(self.display_box, height=400, width=250, state="disabled")
        self.tree = ttk.Treeview(self.display_box, columns=('Option 1', 'Option 2'), show='headings')
        self.tree.heading('Option 1', text='Option 1')
        self.tree.heading('Option 2', text='Option 2')


        self.add_btn = ctk.CTkButton(self, text="Add", command=self.box_selected)
        self.add_btn.grid(row=1, column=0, columnspan=2, sticky='w')

        #self.selected_options.grid(row=0, column=0, sticky='w', pady=(10, 20), padx=10)

        self.tree.grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 20), padx=10)

        #self.selected_options.bind("<Button-1>", lambda e: self.tree.focus_set(self.tree.nearest(e.y)))

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def box_selected(self):
        self.selections[self.box_var.get()] = self.box_var2.get()
        self.tree.insert('', 'end', values=(self.box_var.get(), self.box_var2.get()))
        idx = self.options.index(self.box_var.get())
        self.options.pop(idx)
        print(idx)
        self.box_option.configure(values=self.options) 
        self.box_var.set("")
        self.box_var2.set("")

    def close_dialog_and_reset(self):
        print("close_dialog_and_reset()")
        self.edit.destroy()
        self.delete.destroy()
        print("Delete Button and Edit Button Destroyed")
        self.add_btn.configure(state="normal")
        print("Add Button Re-enabled")
        self.edit = None
        self.delete = None
        print("Edit button and Delete button are None")
        self.is_option_selected = True

    def close_dialog(self):
        print("close_dialog()")
        self.close_dialog_and_reset()

    def edit_option(self):

        def done():
            print("done()")
            self.confirm_edit.destroy()
            self.confirm_edit = None
            self.dialog.destroy()
            print("Edit Dialog Destroyed")
            self.is_option_selected = True
            self.close_dialog()
            

        def confirm_or_cancel():
            self.selections[option1] = self.box_option2_edit_val.get()
            tree_item = self.tree.selection()[0]
            self.tree.delete(tree_item)
            self.tree.unbind('<<TreeviewSelect>>')
            self.tree.insert('', 'end', values=(option1, self.box_option2_edit_val.get()))
            self.tree.bind('<<TreeviewSelect>>', self.on_select)
            self.is_option_selected = True
            done()

            
        selected_item = self.tree.selection()[0]

        option1, option2 = self.tree.item(selected_item, 'values')

        self.dialog = ctk.CTkToplevel(self)

        self.dialog.title("Edit Option 2")
        
        first_opt = ctk.CTkLabel(self.dialog, text=f"{option1}")

        first_opt.grid(row=0, column=0, pady=20)

        self.box_option2_edit_val = ctk.StringVar()
        self.box_option2_edit = ctk.CTkComboBox(self.dialog, values=self.second_options, variable=self.box_option2_edit_val)
        self.box_option2_edit.set(option2)
        self.box_option2_edit.grid(row=0, column=1, pady=20)
        self.confirm_edit = ctk.CTkButton(self.dialog, text="Done", command=confirm_or_cancel)
        self.confirm_edit.grid(row=1, column=0)

    def delete_option(self):
        selected_item = self.tree.selection()[0]
        option1 = self.tree.item(selected_item, 'values')[0]
        self.tree.delete(selected_item)
        self.options.append(option1)
        self.options.sort()
        self.box_option.configure(values=self.options)
        self.selections.pop(option1)
        self.is_option_selected = False
        self.close_dialog()

    def on_select(self, event):
        if self.is_option_selected:
            self.is_option_selected = False
            return
        print("Add Button Disabled")
        self.add_btn.configure(state="disabled")

        print("Edit and Delete buttons created")

        self.edit = ctk.CTkButton(self.display_box, text="Edit", command=self.edit_option)
        self.edit.grid(row=1, column=0, pady=20)

        self.delete = ctk.CTkButton(self.display_box, text="Delete", command=self.delete_option)
        self.delete.grid(row=1, column=1, pady=20)

        self.is_option_selected = True


    
class Test(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Testing")
        self.geometry("800x500")
        self.test_base = Base(self)
        self.test_base.grid()

window = Test()
window.mainloop()