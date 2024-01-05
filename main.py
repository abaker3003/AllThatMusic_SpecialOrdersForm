import tkinter as tk
import subprocess
import datetime
import generators as gn
import xlfile as xl


window = tk.Tk()
window.title("Special Order")

ticket_num = gn.ticketnum()
label = tk.Label(window, text=ticket_num)
label.pack()

data = [ticket_num]

def save_checkbox_value():
    result = [var.get() for var in checkbox_vars]
    print(result)  # Example: Print the selected values to console

checkbox_vars = []
options = ["AEC", "SUD", "OOP"]  # Replace with your options

for option in options:
    varOpt = tk.IntVar(value=1)  # Set initial value if needed
    checkbox_vars.append(varOpt)
    chk = tk.Checkbutton(window, text=option, variable=varOpt)
    chk.pack()

save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.pack()


xl.writeOnXL(data)

window.mainloop()