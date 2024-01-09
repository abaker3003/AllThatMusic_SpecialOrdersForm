import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import subprocess
import datetime
import generators as gn
import xlfile as xl

xl_file = xl.open_excel_file()
window = tk.Tk()
window.geometry("750x750")


ticket_num = gn.ticketnum(xl_file.countRows())
window.title(("Special Order - "+ ticket_num))


data = [ticket_num]

# Executes when save buton is clicked
def save_checkbox_value():
    data.append(cx_name_input.get())
    data.append(cx_phone_input.get())
    data.append(artist_input.get())
    data.append(title_input.get())
    data.append(deposit_input.get())
    data.append(price_input.get())
    data.append(venders.get())
    data.append(typs.get())
    data.append(clerk_input.get())
    xl_file.writeOnXL(data)
    xl_file.close_file()
    save_button.config(text="Saved!")
    save_button['state'] = DISABLED

#--> DISPLAYED <--#

# Date 
date_text = Label(window, text= "Date: " + gn.get_todays_date())
date_text.grid(row=1, column=0)

# Clerk name input
clerk_text = Label(window, text= "Clerk")
clerk_text.grid(row=1, column=4)
clerk_input = Entry(window)
clerk_input.grid(row=1, column=5)


# Title for Venders
venders_text = Label(window, text="Venders")
venders_text.config(font=("Times New Roman", 14))
venders_text.grid(row=3, column=4, sticky='e')

# Radio Button for Venders
venders = StringVar(window, "Venders")
venders_values = ["AEC", "SUD", "OOP"]
for i, vender in enumerate(venders_values): 
    if i < 2:
        rdio_opt = Radiobutton(window, text=vender, variable=venders, value=vender)
        rdio_opt.grid(row=5, column= 4 + i, sticky='w')
    else:
        rdio_opt = Radiobutton(window, text=vender, variable=venders, value=vender)
        rdio_opt.grid(row=6, column= 2 + i, sticky='w')

# Title for Type
type_text = Label(window, text="Type")
type_text.config(font=("Times New Roman", 14))
type_text.grid(row=3, column=1, sticky='e')

# Radio Button for Type
typs = StringVar(window, "Type")
typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
for i, typ in enumerate(typ_values): 
    if i < 2:
        rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
        rdio_typ.grid(row=5, column=i, sticky='w')
    else:
        rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
        rdio_typ.grid(row=6, column=i - 2, sticky='w')

# CX name inpput
cx_name_title = Label(window, text="Name").grid(row=9, column=0)
cx_name_input = Entry(window)
cx_name_input.grid(row=9, column=2)

# Deposit input
deposit_title = Label(window, text="Deposit").grid(row=9, column=5)
deposit_input = Entry(window)
deposit_input.grid(row=10, column=5)

# CX phone number input
cx_phone_title = Label(window, text="Phone").grid(row=12, column=0)
cx_phone_input = Entry(window)
cx_phone_input.grid(row=12, column=2)

# Artist input
artist_title = Label(window, text="Artist").grid(row=14, column=0)
artist_input = Entry(window)
artist_input.grid(row= 14, column=2)

# Price input
price_title = Label(window, text="Price").grid(row=14, column=5)
price_input = Entry(window)
price_input.grid(row=15, column=5)

# Title input
title_title = Label(window, text="Title").grid(row=16, column=0)
title_input = Entry(window)
title_input.grid(row=16, column=2)


save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.grid(row=20, column=3, columnspan=2, padx=20, pady=20)


window.mainloop()