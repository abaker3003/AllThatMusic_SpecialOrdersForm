import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import subprocess
import datetime
import generators as gn
import xlfile as xl

xl_file = xl.open_excel_file()
window = tk.Tk()
window.geometry("500x500")
window.title("Special Order")

ticket_num = gn.ticketnum(xl_file.countRows())
label = tk.Label(window, text=ticket_num)
label.pack()

data = [ticket_num]

def save_checkbox_value():
    result = [var.get() for var in checkbox_vars]
    idx = result.index(1)
    data.append(options[idx])
    result = [var.get() for var in checkbox_types]
    idx = result.index(1)
    data.append(types[idx])
    xl_file.writeOnXL(data)
    xl_file.close_file()

# Trying radio bottons to replace the checkboxex
'''opts = StringVar(window, "Options")
opt_values = {"AEC" : "1",
              "SUD" : "2",
              "OOP" : "3"}
for (text, value) in opt_values.items(): 
    Radiobutton(window, text = text, variable = opts, 
        value = value).pack(side = TOP, ipady = 5)'''

# Checkbox for Option AEC, SUD, OOP
checkbox_vars = []
options = ["AEC", "SUD", "OOP"]  

option_text = Label(window, text="Option")
option_text.config(font = ("Times New Roman", 14))
option_text.pack()

pos = 0
for option in options:
    varOpt = tk.IntVar(value=1)  
    checkbox_vars.append(varOpt)
    chk = tk.Checkbutton(window, text=option, variable=varOpt)
    # Trying to position the checkbox
    chk.pack(padx=pos, pady=1, side=tk.LEFT)
    pos += 1

# Checkbox for type
checkbox_types = []
types = ["CD", "DVD", "LP", "OTHER"]  

type_text = Label(window, text="Type")
type_text.config(font = ("Times New Roman", 14))
type_text.pack()

for t in types:
    varTypes = tk.IntVar(value=1)  
    checkbox_types.append(varTypes)
    chk = tk.Checkbutton(window, text=t, variable=varTypes)
    chk.pack()

save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.pack()


window.mainloop()