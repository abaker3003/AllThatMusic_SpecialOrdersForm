import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class Base(ctk.CTkFrame):
    def __init__(self, *args, header_name="Add Damages", **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ["A", "B", "C", "D", "E"]
        self.second_options = ["1", "2", "3", "4", "5"]

        self.selections = {}

        self.continue_adding = True

        def box_selected():
            choices = self.box_var.get() + ", " + self.box_var2.get()
            self.selections[self.box_var.get()] = self.box_var2.get()
            self.selected_options.configure(state = "normal")
            self.selected_options.insert(tk.END, choices + "\n")
            self.selected_options.configure(state = "disabled")
            idx = self.options.index(self.box_var.get())
            self.options.pop(idx)
            print(idx)
            #self.box_var.
            self.box_var.set("")
            self.box_var2.set("")

        def all_done():
            self.continue_adding = False
            self.add_btn.configure(state="disabled")


            
        while self.continue_adding:
            self.box_var = ctk.StringVar()
            box_option = ctk.CTkComboBox(self, values=self.options, variable=self.box_var)
            box_option.grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 20), padx=10)
            self.box_var2 = ctk.StringVar()
            box_option2 = ctk.CTkComboBox(self, values=self.second_options, variable=self.box_var2)
            box_option2.grid(row=0, column=2, columnspan=2, sticky='w', pady=(10, 20), padx=10)


            self.display_box = ctk.CTkFrame(self, height=500, width=300)
            self.display_box.grid(row=0, column=4, sticky='w', pady=(10, 20), padx=10)

            self.selected_options = ctk.CTkTextbox(self.display_box, height=400, width=250, state="disabled")

            self.add_btn = ctk.CTkButton(self, text="Add", command=box_selected)
            self.add_btn.grid(row=1, column=0, columnspan=2, sticky='w')

            self.selected_options.grid(row=0, column=0, sticky='w', pady=(10, 20), padx=10)

            done_btn = ctk.CTkButton(self, text="Done", command=all_done)
    
class Test(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Testing")
        self.geometry("800x900")
        self.test_base = Base(self)
        self.test_base.grid()

window = Test()
window.mainloop()