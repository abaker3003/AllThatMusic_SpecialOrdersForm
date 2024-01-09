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
    data.append(opts.get())
    data.append(typs.get())
    data.append(cx_name_input.get())
    data.append(cx_phone_input.get())
    xl_file.writeOnXL(data)
    xl_file.close_file()
    save_button.config(text="Saved!")
    save_button['state'] = DISABLED


option_text = Label(window, text="Option")
option_text.config(font=("Times New Roman", 14))
option_text.grid(row=1, column=0, padx=10, pady=10, sticky='e')

opts = StringVar(window, "Options")
opt_values = ["AEC", "SUD", "OOP"]
for i, opt in enumerate(opt_values): 
    rdio_opt = Radiobutton(window, text=opt, variable=opts, value=opt)
    rdio_opt.grid(row=i+2, column=0, padx=10, pady=5, sticky='w')

type_text = Label(window, text="Type")
type_text.config(font=("Times New Roman", 14))
type_text.grid(row=1, column=1, padx=10, pady=10, sticky='e')

typs = StringVar(window, "Type")
typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
for i, typ in enumerate(typ_values): 
    rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
    rdio_typ.grid(row=i+2, column=1, padx=10, pady=5, sticky='w')

cx_name_title = Label(window, text="Name").grid(column=2, row=1)
cx_name_input = Entry(window)
cx_name_input.grid(column=3, row=1)

cx_phone_title = Label(window, text="Phone").grid(column=2, row=2)
cx_phone_input = Entry(window)
cx_phone_input.grid(column=3, row=2)

save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.pack()


window.mainloop()