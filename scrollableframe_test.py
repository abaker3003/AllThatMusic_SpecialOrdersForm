import customtkinter as ctk
import tkinter as tk
from tkinter import ttk

class app(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.title('Scrollable Frame Test')
        #(width, height)
        self.geometry('650x400')
        self.scrollable_frame = ctk.CTkScrollableFrame(self, orientation="horizontal", height= 300, width=600)
        self.scrollable_frame.grid(row=0, column=0,sticky='nsew')

        #frame for column titles
        self.frame = ctk.CTkFrame(self.scrollable_frame)
        self.frame.grid(row=0, column=0, sticky='nsew')

        for i in range(10):
            ## PADX NEEDS TO BE THE SAME AS
            ## THE RADIO BUTTONS TO BE ALIGNED
            ctk.CTkLabel(self.frame, text=f'Column {i}', width=130).grid(row=0, column=i, sticky='nsew', padx=5, pady=5)

        #frame for results
        self.results = ctk.CTkFrame(self)

        # frame for data per column
        self.data = ctk.CTkScrollableFrame(self.scrollable_frame, orientation="vertical", height=250)

        self.selection = ctk.StringVar()

        for i in range(10):

            for j in range(10):
                ## PADX NEEDS TO BE THE SAME AS
                ## THE LABELS TO BE ALIGNED
                ctk.CTkRadioButton(self.data, text=f'Row {j}, Column {i}', width=130, variable=self.selection, command=lambda idx=[i,j]: show_selected(idx)).grid(row=j, column=i, sticky='nsew', pady=10, padx=(5,5))

        self.data.grid(row=1, column=0, sticky='nsew')

        def show_selected(idx):
            ctk.CTkLabel(self.results, text=f'Row {idx[1]}, Column {idx[0]}', width=100, font=("Arial", 35)).grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        
        self.results.grid(row=1, column=0, sticky='nsew')
        self.results.columnconfigure(0, weight=1)
        self.results.rowconfigure(0, weight=1)
        self.results_label = ctk.CTkLabel(self.results, text='Results', width=100)
        self.results_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)



window = app()
window.mainloop()