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
window.title("Special Order - ", ticket_num)


data = [ticket_num]


def save_checkbox_value():
    data.append(venders.get())
    data.append(typs.get())
    data.append(cx_name_input.get())
    data.append(cx_phone_input.get())
    xl_file.writeOnXL(data)
    xl_file.close_file()
    save_button.config(text="Saved!")
    save_button['state'] = DISABLED


venders_text = Label(window, text="Venders")
venders_text.config(font=("Times New Roman", 14))
venders_text.grid(row=1, column=6, padx=10, pady=10, sticky='e')

venders = StringVar(window, "Venders")
venders_values = ["AEC", "SUD", "OOP"]
for i, vender in enumerate(venders_values): 
    rdio_opt = Radiobutton(window, text=vender, variable=venders, value=vender)
    rdio_opt.grid(row=1, column=7 + i, padx=10, pady=5, sticky='w')

type_text = Label(window, text="Type")
type_text.config(font=("Times New Roman", 14))
type_text.grid(row=2, column=0, padx=10, pady=10, sticky='e')

typs = StringVar(window, "Type")
typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
for i, typ in enumerate(typ_values): 
    rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
    rdio_typ.grid(row=2, column=1 + i, padx=10, pady=5, sticky='w')

cx_name_title = Label(window, text="Name").grid(column=2, row=1)
cx_name_input = Entry(window)
cx_name_input.grid(row=2, column=1)

cx_phone_title = Label(window, text="Phone").grid(column=2, row=2)
cx_phone_input = Entry(window)
cx_phone_input.grid(row=2, column=1)

save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.grid(row=len(typ_values)+3, column=0, columnspan=2, padx=10, pady=10)


window.mainloop()