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


ticket_num = gn.ticketnum(xl_file.countRows())
window.title(("Special Order - "+ ticket_num))


data = [ticket_num]

# Executes when save buton is clicked
def save_checkbox_value():
    data.append(venders.get())
    data.append(typs.get())
    data.append(cx_name_input.get())
    data.append(cx_phone_input.get())
    xl_file.writeOnXL(data)
    xl_file.close_file()
    save_button.config(text="Saved!")
    save_button['state'] = DISABLED

#--> DISPLAYED <--#

# Date 
date_text = Label(window, text= "Date: " + gn.get_todays_date())
date_text.grid(row=0, column=0)

# Clerk name input
clerk_text = Label(window, text= "Clerk")
clerk_text.grid(row=0, column=6)
clerk_input = Entry(window)
clerk_input.grid(row=0, column=7)


# Title for Venders
venders_text = Label(window, text="Venders")
venders_text.config(font=("Times New Roman", 14))
venders_text.grid(row=1, column=6, sticky='e')

# Radio Button for Venders
venders = StringVar(window, "Venders")
venders_values = ["AEC", "SUD", "OOP"]
for i, vender in enumerate(venders_values): 
    rdio_opt = Radiobutton(window, text=vender, variable=venders, value=vender)
    rdio_opt.grid(row=1, column=7 + i, sticky='w')

# Title for Type
type_text = Label(window, text="Type")
type_text.config(font=("Times New Roman", 14))
type_text.grid(row=1, column=0, sticky='e')

# Radio Button for Type
typs = StringVar(window, "Type")
typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
for i, typ in enumerate(typ_values): 
    rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
    rdio_typ.grid(row=2, column=1 + i, sticky='w')

# CX name inpput
cx_name_title = Label(window, text="Name").grid(row=6, column=0)
cx_name_input = Entry(window)
cx_name_input.grid(row=6, column=2)

# CX phone number input
cx_phone_title = Label(window, text="Phone").grid(row=8, column=0)
cx_phone_input = Entry(window)
cx_phone_input.grid(row=8, column=2)

save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.grid(row=len(typ_values)+3, column=0, columnspan=2, padx=10, pady=10)


window.mainloop()