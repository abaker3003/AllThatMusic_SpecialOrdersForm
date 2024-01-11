import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as msgbox

from matplotlib import artist
import generators as gn
import xlfile as xl

xl_file = xl.open_excel_file()
window = tk.Tk()
window.geometry("500x225")


ticket_num = gn.ticketnum(xl_file.countRows())
window.title(("Special Order - "+ ticket_num))


data = [ticket_num]

def check_form_complete():
    # Check if all required entries have text
    if not cx_name_input.get() or not cx_phone_input.get() or not artist_input.get() or not title_input.get() or not deposit_input.get() or not price_input.get():
        return False

    # Check if at least one vendor and type radio button is selected
    if not vendors.get() or not typs.get():
        return False

    return True

def check_proper_info():
    proper = True
    errormsg = ''
    num_of_msgs = 1
    if not cx_name_input.get().isalpha():
        errormsg += str(num_of_msgs) + ': Customer name must be all letters.\n'
        proper = False
        num_of_msgs += 1
    if not cx_phone_input.get().isdigit():
        errormsg += str(num_of_msgs) + ': Phone number must be numbers only.\n'
        proper = False
        num_of_msgs += 1
    if len(cx_phone_input.get()) != 10:
        errormsg += str(num_of_msgs) + ": Phone number must be exactly 10 digits long.\n"
        proper = False
        num_of_msgs += 1
    if not deposit_input.get().isdigit() and '.' not in deposit_input.get():
        errormsg += str(num_of_msgs) + ": Deposit amount should not contain any other symbols except decimal.\n"
        proper = False
        num_of_msgs += 1
    if not price_input.get().isdigit() and '.' not in price_input.get():
        errormsg += str(num_of_msgs) + ": Price amount should not contain any other symbols except decimal.\n"
        proper = False
        num_of_msgs += 1
    return proper, errormsg

# Executes when save buton is clicked
def save_checkbox_value():

    if not check_form_complete():
        msgbox.showerror("Error", "Please fill out the entire form.")
        return
    proper, msg = check_proper_info()
    if not proper:
        msgbox.showwarning("Error", msg)
        return
    
    data.append(cx_name_input.get())
    data.append(cx_phone_input.get())
    data.append(artist_input.get())
    data.append(title_input.get())
    data.append(deposit_input.get())
    data.append(price_input.get())
    data.append(vendors.get())
    data.append(typs.get())
    data.append(clerk_input.get())
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
clerk_text.grid(row=0, column=4)
clerk_input = Entry(window)
clerk_input.grid(row=0, column=5)


# Title for Venders
vendors_text = Label(window, text="Vendors")
vendors_text.config(font=("Times New Roman", 14))
vendors_text.grid(row=2, column=4, sticky='e')

# Radio Button for Venders
vendors = StringVar(window, "Vendors")
vendors_values = ["AEC", "AMS", "AMA"]
for i, vendor in enumerate(vendors_values): 
    if i < 2:
        rdio_opt = Radiobutton(window, text=vendor, variable=vendors, value=vendor)
        rdio_opt.grid(row=4, column= 4 + i, sticky='w')
    else:
        rdio_opt = Radiobutton(window, text=vendor, variable=vendors, value=vendor)
        rdio_opt.grid(row=5, column= 2 + i, sticky='w')

# Title for Type
type_text = Label(window, text="Type")
type_text.config(font=("Times New Roman", 14))
type_text.grid(row=2, column=1, sticky='e')

# Radio Button for Type
typs = StringVar(window, "Type")
typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
for i, typ in enumerate(typ_values): 
    if i < 2:
        rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
        rdio_typ.grid(row=4, column=i, sticky='w')
    else:
        rdio_typ = Radiobutton(window, text=typ, variable=typs, value=typ)
        rdio_typ.grid(row=5, column=i - 2, sticky='w')

# CX name inpput
cx_name_title = Label(window, text="Name")
cx_name_title.grid(row=6, column=0)
cx_name_input = Entry(window)
cx_name_input.grid(row=6, column=2)

# Deposit input
deposit_title = Label(window, text="Deposit")
deposit_title.grid(row=6, column=5)
deposit_input = Entry(window)
deposit_input.grid(row=7, column=5)

# CX phone number input
cx_phone_title = Label(window, text="Phone")
cx_phone_title.grid(row=7, column=0)
cx_phone_input = Entry(window)
cx_phone_input.grid(row=7, column=2)

# Artist input
artist_title = Label(window, text="Artist")
artist_title.grid(row=8, column=0)
artist_input = Entry(window)
artist_input.grid(row= 8, column=2)

# Price input
price_title = Label(window, text="Price")
price_title.grid(row=8, column=5)
price_input = Entry(window)
price_input.grid(row=9, column=5)

# Title input
title_title = Label(window, text="Title")
title_title.grid(row=9, column=0)
title_input = Entry(window)
title_input.grid(row=9, column=2)


save_button = tk.Button(window, text="Save", command=save_checkbox_value)
save_button.grid(row=10, column=2, columnspan=2, padx=20, pady=20)


window.mainloop()