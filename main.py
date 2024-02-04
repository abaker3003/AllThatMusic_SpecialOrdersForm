import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from tkinter.ttk import *
from tkinter.tix import *
import tkinter.messagebox as msgbox
import customtkinter as ctk
from matplotlib import artist
import generators as gn
import xlfile as xl
import ai_project as ai

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
class Base(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

class SOForm(Base):
    def __init__(self, master=None):
        super().__init__(master)
        xl_file = xl.open_excel_file('SO_Test.xlsx')

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
        
        row_offset = 0  # Initialize row offset for better readability

        # Date 
        date_text = ctk.CTkLabel(self, text= "Date: " + todays_date, text_color="#000", font=("Roboto", 16))
        date_text.grid(row=row_offset, column=2, columnspan=1, pady=(10, 0))

        # Clerk name input
        clerk_text = ctk.CTkLabel(self, text= "Clerk", text_color="#000", font=("Roboto", 16))
        clerk_text.grid(row=row_offset, column=3)
        clerk_input = ctk.CTkEntry(self)
        clerk_input.grid(row=row_offset, column=4, sticky="ew", padx=10)

        row_offset += 1  # Increment row offset 

        # Divider
        divider = Separator(self, orient='horizontal')
        divider.grid(row=row_offset, column=1, columnspan=6, sticky='ew', pady=10)

        row_offset += 1  # Increment row offset 

        # Title for Vendors
        vendors_text = ctk.CTkLabel(self, text="Vendors",font=("Roboto", 16), text_color="#000")
        vendors_text.grid(row=row_offset, column=4, pady=(10, 0))
        # Radio Button for Vendors
        vendors = StringVar(self, "Vendors")
        vendors_values = ["AEC", "AMS", "AMA"]

        row_offset += 1  # Increment row offset

        # Button positioning based on amount of options
        for i, vendor in enumerate(vendors_values): 
            if i < 2:
                rdio_opt = ctk.CTkRadioButton(self, text=vendor, variable=vendors, value=vendor, text_color="#000", font=("Roboto", 16))
                rdio_opt.grid(row=row_offset, column= 4 + i, sticky='w')
            else:
                rdio_opt = ctk.CTkRadioButton(self, text=vendor, variable=vendors, value=vendor, text_color="#000", font=("Roboto", 16))
                rdio_opt.grid(row=row_offset + 1, column= 3 + i, sticky='w')

        # Title for Type
        type_text = ctk.CTkLabel(self, text="Type", font=("Roboto", 16), text_color="#000")
        type_text.grid(row=row_offset - 1, column=2, pady=(10, 0))

        # Radio Button for Type
        typs = StringVar(self, "Type")
        typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]

        # Button positioning based on amount of options
        for i, typ in enumerate(typ_values): 
            if i < 3:
                rdio_typ = ctk.CTkRadioButton(self, text=typ, variable=typs, value=typ, text_color="#000", font=("Roboto", 16))
                rdio_typ.grid(row=row_offset, column=i + 1, sticky='w')
            else:
                rdio_typ = ctk.CTkRadioButton(self, text=typ, variable=typs, value=typ, text_color="#000", font=("Roboto", 16))
                rdio_typ.grid(row=row_offset + 1, column=i - 2, sticky='w')

        row_offset += 2  # Increment row offset 

        # Divider
        divider = Separator(self, orient='horizontal')
        divider.grid(row=row_offset, column=0, columnspan=7, sticky='ew', pady=10)
        row_offset += 2  # Increment row offset

        # CX name inpput
        cx_name_title = ctk.CTkLabel(self, text="Name", text_color="#000", font=("Roboto", 16))
        cx_name_title.grid(row=row_offset, column=2)
        cx_name_input = ctk.CTkEntry(self)
        cx_name_input.grid(row=row_offset + 1, column=2, padx=10)

        # CX phone number input
        cx_phone_title = ctk.CTkLabel(self, text="Phone", text_color="#000", font=("Roboto", 16))
        cx_phone_title.grid(row=row_offset, column=3)
        cx_phone_input = ctk.CTkEntry(self)
        cx_phone_input.grid(row=row_offset + 1, column=5, padx=10)

        row_offset += 2  # Increment row offset

        # Artist input
        artist_title = ctk.CTkLabel(self, text="Artist", text_color="#000", font=("Roboto", 16))
        artist_title.grid(row=row_offset, column=2)
        artist_input = ctk.CTkEntry(self)
        artist_input.grid(row=row_offset + 1, column=2, padx=10)

        # Title input
        title_title = ctk.CTkLabel(self, text="Title", text_color="#000", font=("Roboto", 16))
        title_title.grid(row=row_offset, column=4)
        title_input = ctk.CTkEntry(self)
        title_input.grid(row=row_offset + 1, column=4, padx=10)

        row_offset += 2  # Increment row offset

        # Deposit input
        deposit_title = ctk.CTkLabel(self, text="Deposit", text_color="#000", font=("Roboto", 16))
        deposit_title.grid(row=row_offset, column=2)
        deposit_input = ctk.CTkEntry(self)
        deposit_input.grid(row=row_offset + 1, column=2, padx=10)

        # Price input
        price_title = ctk.CTkLabel(self, text="Price", text_color="#000", font=("Roboto", 16))
        price_title.grid(row=row_offset, column=4)
        price_input = ctk.CTkEntry(self)
        price_input.grid(row=row_offset + 1, column=4, padx=10)

        row_offset += 2  # Increment row offset


        save_button = ctk.CTkButton(self, text="Save", command=save_checkbox_value, text_color="#000", font=("Roboto", 16))
        save_button.grid(row=row_offset, column=2, pady=20, sticky='ew')

        back_button = ctk.CTkButton(self, text="Cancel", command=go_back, text_color="#000", font=("Roboto", 16))
        back_button.grid(row=row_offset, column=4, pady=20, sticky='ew')

class PrevSO(Base):
    def __init__(self, master=None):
        super().__init__(master)
        self.configure(background="white")
        self.prev_so = ctk.CTkLabel(self, text="Previous Special Orders", text_color="black", font=("Arial", 16))
        self.prev_so.grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 20), padx=10)

        # Load the Excel file into a pandas DataFrame
        self.excel_file = xl.open_excel_file('SO_Test.xlsx')
        self.df = self.excel_file.read_into_dataframe_SO()

        # Create the Treeview
        self.tree = Treeview(self, columns=list(self.df.columns), show="headings")
        for column in self.df.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=100, anchor='center')  # Adjust width and centering as needed
        self.tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

        # Add the data to the Treeview
        for _, row in self.df.iterrows():
            self.tree.insert('', 'end', values=list(row))

        # Configure the grid to expand the treeview with window resizing
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)


        # Create the Scrollbar
        self.scrollbar_y = Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.scrollbar_y.grid(row=1, column=1, sticky='ns', padx=(0, 10), pady=5)
        self.scrollbar_x = Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.scrollbar_x.grid(row=2, column=0, sticky='ew', padx=10, pady=(0, 10))
        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)
        
        # Back Button with CTk Improvement
        self.back_button = ctk.CTkButton(self,
                                        text="Back",
                                        command=self.master.show_main_frame,
                                        text_color="#000")
        self.back_button.grid(row=3, column=0, padx=10, pady=20, sticky='w')

        
        # Bind the double-click event
        self.tree.bind('<Double-1>', self.on_double_click)

        self.dialog = None
        self.save_changes_button = None

    def on_double_click(self, event):
        # Get the selected item
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')

        # Create a dialog with entry fields for each column
        self.dialog = ctk.CTkToplevel(self)
        self.dialog.title("Edit Order")
        entries = {}

        typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
        vendors_values = ["AEC", "AMS", "AMA"]

        for i, column in enumerate(self.df.columns):
            ctk.CTkLabel(self.dialog, text=column, font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5)
                
            if column == "VENDOR":
                entry = ctk.CTkOptionMenu(self.dialog, values=vendors_values)
                entry.set(values[i])  # Set to current value or default one
                entry.grid(row=i, column=1, padx=10, pady=5)
            elif column == "TYPE":
                entry = ctk.CTkOptionMenu(self.dialog, values=typ_values)
                entry.set(values[i])  # Set to current value or default one
                entry.grid(row=i, column=1, padx=10, pady=5)
            else:
                entry = ctk.CTkEntry(self.dialog)
                entry.insert(0, values[i])
                entry.grid(row=i, column=1, padx=10, pady=5)

            if column in set(["REF NUM", "DATE", "CLERK NAME"]):
                entry.configure(state='disabled')
            
            entries[column] = entry

        self.save_changes_button = ctk.CTkButton(self.dialog,
                                                text="Save",
                                                command=lambda: self.save(item, entries))
        self.save_changes_button.grid(row=len(self.df.columns), column=0, columnspan=2, pady=20)

        self.cancel_changes_button = ctk.CTkButton(self.dialog, text="Back", command=self.dialog.destroy)
        self.cancel_changes_button.grid(row=len(self.df.columns) + 1, column=0, columnspan=2, pady=20)

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
        new_values = [entries[column].get() for column in self.df.columns]
        self.tree.item(item, values=new_values)
        
        # Assuming that 'I004' format means 'I' followed by an actual index number
        if item.startswith('I') and item[1:].isdigit():
            item_index = int(item[1:])
        else:
            # Handle the case where item does not follow the expected format
            raise ValueError(f"The item identifier {item} is not in the expected format.")

        
        for column, new_value in zip(self.df.columns, new_values):
            self.df.at[item_index, column] = new_value  # Make sure to use at[item_index, column]

        # Write the DataFrame back to the Excel file
        self.excel_file.update_excel(item_index + 1, new_values)  # Add 1 if necessary for Excel indexing

        self.save_changes_button.configure(text="Saved!", state=DISABLED)
        self.cancel_changes_button.configure(text="Back")

        # Destroy the dialog
        self.dialog.destroy()
        self.dialog = None


class SOApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Special Order")
        self.geometry("1200x680")
        self.configure(background="#350909")

        self.sidebar_menu = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_menu.grid(row=0, column=0, sticky='nsew', rowspan=8)
        self.sidebar_menu.grid_rowconfigure(4, weight=1)

        self.special_order_form = SOForm(self)
        self.previous_orders = PrevSO(self)
        self.ai_form = ai(self)
        self.reconciliation_form = NONE

        self.special_order_form_button = ctk.CTkButton(self, text="Special Order Form", command=self.show_special_order_form, fg_color="#000000", border_color="red", font=("Arial", 30))
        self.previous_orders_button = ctk.CTkButton(self, text="Previous Orders", command=self.show_previous_orders, fg_color="#000000", border_color="red", font=("Arial", 30))
        self.ai_form_button = ctk.CTkButton(self, text="AI Form", command=self.show_ai_form, fg_color="#000000", border_color="red", font=("Arial", 30))
        self.reconciliation_form_button = ctk.CTkButton(self, text="Reconciliation Form", command=self.show_reconciliation_form, fg_color="#000000", border_color="red", font=("Arial", 30))

        self.hide_all_frames()

        self.special_order_form_button.grid(row=2,column=0)
        self.previous_orders_button.grid(row=3,column=0)
        self.ai_form_button.grid(row=4,column=0)
        self.reconciliation_form_button.grid(row=5,column=0)

    def hide_all_frames(self):
        for frame in [self.special_order_form, self.previous_orders]:
            frame.grid_forget()

    def show_special_order_form(self):
        self.configure(background="#ffced0")
        self.hide_all_frames()
        self.special_order_form.grid()
        self.special_order_form_button["state"]="disabled"

    def show_previous_orders(self):
        self.hide_all_frames()
        self.previous_orders.grid()
        self.previous_orders_button["state"]="disabled"

    def show_ai_form(self):
        self.hide_all_frames()
        self.ai_form.grid()
        self.ai_form_button["state"]="disabled"

    def show_reconciliation_form(self):
        self.hide_all_frames()
        self.reconciliation_form.grid()
        self.reconciliation_form_button["state"]="disabled"

    def show_main_frame(self):
        self.hide_all_frames()
        # Show the main application frame
        self.previous_orders_button.grid()
        self.special_order_form_button.grid()
    
    

window = SOApp()
window.mainloop()