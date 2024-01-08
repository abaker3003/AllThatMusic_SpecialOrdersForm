import tkinter as tk
import subprocess
import datetime
import generators as gn
import xlfile as xl

xl_file = xl.open_excel_file()
window = tk.Tk()
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

checkbox_vars = []
options = ["AEC", "SUD", "OOP"]  # Replace with your options

for option in options:
    varOpt = tk.IntVar(value=1)  # Set initial value if needed
    checkbox_vars.append(varOpt)
    chk = tk.Checkbutton(window, text=option, variable=varOpt)
    chk.pack()

checkbox_types = []
types = ["CD", "DVD", "LP", "OTHER"]  # Replace with your options

for t in types:
    varTypes = tk.IntVar(value=1)  # Set initial value if needed
    checkbox_types.append(varTypes)
    chk = tk.Checkbutton(window, text=t, variable=varTypes)
    chk.pack()

save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.pack()


window.mainloop()