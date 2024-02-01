import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from tkinter.ttk import *
from tkinter.tix import *
import tkinter.messagebox as msgbox
from matplotlib import artist
import generators as gn
import xlfile as xl

class Base(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

class SOForm(Base):
    def __init__(self, master=None):
        super().__init__(master)
        xl_file = xl.open_excel_file()

        # Generating current date
        todays_date = gn.get_todays_date()

        # Generating ticket number
        ticket_num = gn.ticketnum(xl_file)

        if master is not None:
            master.title(("Special Order - "+ ticket_num))
        else:
            self.Label(self, "Special Order - "+ ticket_num)


        # Adding the current date and ticket number to data list
        data = [todays_date, ticket_num]

        # Checks if all input fields are filled
        def check_form_complete():
            # Check if all required entries have text
            if not cx_name_input.get() or not cx_phone_input.get() or not artist_input.get() or not title_input.get() or not deposit_input.get() or not price_input.get():
                return False

            # Check if at least one vendor and type radio button is selected
            if not vendors.get() or not typs.get():
                return False

            return True

        # Checks to see if each field input is correct
        def check_proper_info():
            proper = True
            errormsg = ''
            num_of_msgs = 1
            if " " in cx_name_input.get():
                cx_names = cx_name_input.get().split(" ")
                for name in cx_names:
                    if not name.isalpha():
                        errormsg += str(num_of_msgs) + ': Customer name must be all letters.\n'
                        proper = False
                        num_of_msgs += 1
                        break
            elif not cx_name_input.get().isalpha():
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
            data.append(float(deposit_input.get()))
            data.append(float(price_input.get()))
            data.append(vendors.get())
            data.append(typs.get())
            data.append(clerk_input.get())
            xl_file.writeOnXL(data)
            xl_file.close_file()
            save_button.config(text="Saved!")
            save_button['state'] = DISABLED
            back_button.config(text="Back")

        def go_back():
            xl_file.close_file()
            self.master.show_main_frame()


        #--> DISPLAYED <--#

        # Date 
        date_text = Label(self, text= "Date: " + todays_date)
        date_text.grid(row=0, column=0)

        # Clerk name input
        clerk_text = Label(self, text= "Clerk")
        clerk_text.grid(row=0, column=4)
        clerk_input = Entry(self)
        clerk_input.grid(row=0, column=5)

        # Title for Vendors
        vendors_text = Label(self, text="Vendors")
        vendors_text.config(font=("Times New Roman", 14))
        vendors_text.grid(row=2, column=4, sticky='e')

        # Radio Button for Vendors
        vendors = StringVar(self, "Vendors")
        vendors_values = ["AEC", "AMS", "AMA"]

        # Button positioning based on amount of options
        for i, vendor in enumerate(vendors_values): 
            if i < 2:
                rdio_opt = Radiobutton(self, text=vendor, variable=vendors, value=vendor)
                rdio_opt.grid(row=4, column= 4 + i, sticky='w')
            else:
                rdio_opt = Radiobutton(self, text=vendor, variable=vendors, value=vendor)
                rdio_opt.grid(row=5, column= 2 + i, sticky='w')

        # Title for Type
        type_text = Label(self, text="Type")
        type_text.config(font=("Times New Roman", 14))
        type_text.grid(row=2, column=1, sticky='e')

        # Radio Button for Type
        typs = StringVar(self, "Type")
        typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]

        # Button positioning based on amount of options
        for i, typ in enumerate(typ_values): 
            if i < 2:
                rdio_typ = Radiobutton(self, text=typ, variable=typs, value=typ)
                rdio_typ.grid(row=4, column=i, sticky='w')
            else:
                rdio_typ = Radiobutton(self, text=typ, variable=typs, value=typ)
                rdio_typ.grid(row=5, column=i - 2, sticky='w')

        # CX name inpput
        cx_name_title = Label(self, text="Name")
        cx_name_title.grid(row=6, column=0)
        cx_name_input = Entry(self)
        cx_name_input.grid(row=6, column=2)

        # Deposit input
        deposit_title = Label(self, text="Deposit")
        deposit_title.grid(row=6, column=5)
        deposit_input = Entry(self)
        deposit_input.grid(row=7, column=5)

        # CX phone number input
        cx_phone_title = Label(self, text="Phone")
        cx_phone_title.grid(row=7, column=0)
        cx_phone_input = Entry(self)
        cx_phone_input.grid(row=7, column=2)

        # Artist input
        artist_title = Label(self, text="Artist")
        artist_title.grid(row=8, column=0)
        artist_input = Entry(self)
        artist_input.grid(row= 8, column=2)

        # Price input
        price_title = Label(self, text="Price")
        price_title.grid(row=8, column=5)
        price_input = Entry(self)
        price_input.grid(row=9, column=5)

        # Title input
        title_title = Label(self, text="Title")
        title_title.grid(row=9, column=0)
        title_input = Entry(self)
        title_input.grid(row=9, column=2)


        save_button = tk.Button(self, text="Save", command=save_checkbox_value)
        save_button.grid(row=10, column=2, columnspan=1, padx=20, pady=20)

        back_button = tk.Button(self, text="Cancel", command=go_back)
        back_button.grid(row=10, column=1, columnspan=1, padx=20, pady=20)

class PrevSO(Base):
    def __init__(self, master=None):
        super().__init__(master)
        #self.geometry("750x750")
        self.prev_so = tk.Label(self, text="Previous Special Orders")
        self.prev_so.grid(row=0, column=0, sticky='w')

        # Load the Excel file into a pandas DataFrame
        self.excel_file = xl.open_excel_file()
        self.df = self.excel_file.read_into_dataframe()

        # Create the Treeview
        self.tree = Treeview(self, columns=list(self.df.columns), show="headings")
        for column in self.df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=50, minwidth=20)  # Adjust width as needed
            self.tree.grid(row=1, column=0, sticky='nsew')
        # Add the data to the Treeview
        for _, row in self.df.iterrows():
            self.tree.insert('', 'end', values=list(row))

        # Create the Scrollbar
        self.scrollbar_y = Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.scrollbar_y.grid(row=1, column=1, sticky='ns')
        self.scrollbar_x = Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.scrollbar_x.grid(row=2, column=0, sticky='ew')
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.cancel_changes_button = Button(self, text="Back", command=self.master.show_main_frame)
        self.cancel_changes_button.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky='s')

        # Bind the double-click event
        self.tree.bind('<Double-1>', lambda event: self.on_double_click())

        self.dialog = None
        self.save_changes_button = None

    def on_double_click(self):
        # Get the selected item
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')

        # Create a dialog with entry fields for each column
        self.dialog = Toplevel(self)
        self.dialog.title("Edit Order")
        entries = []
        for i, (column, value) in enumerate(zip(self.df.columns, values)):
            label = Label(self.dialog, text=column)
            label.grid(row=i, column=0)
            entry = Entry(self.dialog)
            entry.insert(0, value)
            entry.grid(row=i, column=1)
            entries.append(entry)

        self.save_changes_button = Button(self.dialog, text="Save", command=lambda: self.save(item, entries))
        self.save_changes_button.grid(row=len(self.df.columns), column=0, columnspan=2)

        #self.df['PHONE'] = self.df['PHONE'].astype(str).round()


    def on_edit(self):
        # Get the edited item and column
        item = self.tree.selection()[0]
        column = self.tree.focus_column()
        new_value = self.tree.set(item, column)

        # Update the DataFrame and the Excel file
        self.df.loc[int(item), column] = new_value
        self.excel_file.update_excel(int(item) + 1, [new_value])

    def save(self, item, entries):
        # Update the Treeview and the DataFrame with the new values
        new_values = [entry.get() for entry in entries]
        self.tree.item(item, values=new_values)
        for column, value in zip(self.df.columns, new_values):
            self.df.loc[self.df[column] == value, column] = value

        # Convert the item variable to an integer
        item = int(item)

        # Write the DataFrame back to the Excel file
        self.excel_file.update_excel(item + 1, new_values)

        self.save_changes_button.config(text="Saved!", state=DISABLED)
        self.cancel_changes_button.config(text="Back")

        # Destroy the dialog
        self.dialog.destroy()
        self.dialog = None


class SOApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Special Order")
        self.geometry("550x325")

        self.special_order_form = SOForm(self)
        self.previous_orders = PrevSO(self)

        self.special_order_form_button = tk.Button(self, text="Special Order Form", command=self.show_special_order_form)
        self.previous_orders_button = tk.Button(self, text="Previous Orders", command=self.show_previous_orders)

        self.hide_all_frames()

        self.special_order_form_button.pack()
        self.previous_orders_button.pack()

    def hide_all_frames(self):
        for frame in [self.special_order_form, self.previous_orders]:
            frame.pack_forget()
        self.previous_orders_button.pack_forget()
        self.special_order_form_button.pack_forget()

    def show_special_order_form(self):
        self.hide_all_frames()
        self.special_order_form.pack()

    def show_previous_orders(self):
        self.hide_all_frames()
        self.previous_orders.pack()

    def show_main_frame(self):
        self.hide_all_frames()
        # Show the main application frame
        self.previous_orders_button.pack()
        self.special_order_form_button.pack()
    
    

window = SOApp()
window.mainloop()