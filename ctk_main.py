'''import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from tkinter.ttk import *
from tkinter.tix import *
import tkinter.messagebox as msgbox'''
import customtkinter as ctk
from matplotlib import artist
import generators as gn
import xlfile as xl
import ai_project as ai

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SO_Form(ctk.CTkFrame):
    def __init__(self, *args, header_name="Special Order Form", **kwargs):
        super().__init__(*args, **kwargs)

        xl_file = xl.open_excel_file('SO_Test.xlsx')

        # Generating current date
        todays_date = gn.get_todays_date()

        # Generating ticket number
        ticket_num = gn.ticketnum(xl_file)

        self.header_name = header_name + " - " + ticket_num

        self.header = ctk.CTkLabel(self, text=self.header_name, font=("Arial", 20))
        self.header.grid(row=0, column=1, columnspan=2, sticky='w', pady=(10, 20), padx=10)


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
                ctk.msgbox.showerror("Error", "Please fill out the entire form.")
                return
            proper, msg = check_proper_info()
            if not proper:
                ctk.msgbox.showwarning("Error", msg)
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
            if ship_var.get() == 1:
                data.append("Yes")
                data.extend(self.shipping_data)
            xl_file.writeOnXL(data)
            xl_file.close_file()
            save_button.configure(text="Saved!")
            save_button['state'] = "DISABLED"
            back_button.configure(text="Back")

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

        def open_shipping_window():
            shipping_window = ctk.CTkToplevel(self)
            shipping_window.title("Shipping Information")

            def check_shipping_info_complete():
                if not address_input.get() or not city_input.get() or not zipcode_input.get() or not state_select.get():
                    return False
                return True
            
            def check_proper_info():
                proper = True
                errormsg = ''
                num_of_msgs = 1
                if not address_input.get():
                    errormsg += str(num_of_msgs) + ': Address cannot be empty.\n'
                    proper = False
                    num_of_msgs += 1
                if not city_input.get().isalpha():
                    errormsg += str(num_of_msgs) + ': City input is invalid.\n'
                    proper = False
                    num_of_msgs += 1
                if not zipcode_input.get().isdigit():
                    errormsg += str(num_of_msgs) + ': Zip code must be numbers only.\n'
                    proper = False
                    num_of_msgs += 1
                if len(zipcode_input.get()) != 5:
                    errormsg += str(num_of_msgs) + ": Zip code must be exactly 5 digits long.\n"
                    proper = False
                    num_of_msgs += 1
                if not state_select.get():
                    errormsg += str(num_of_msgs) + ': State cannot be empty.\n'
                    proper = False
                    num_of_msgs += 1
                return proper, errormsg
            
            def save_shipping_info():
                if not check_shipping_info_complete():
                    ctk.msgbox.showerror("Error", "Please fill out the entire form.")
                    return
                proper, msg = check_proper_info()
                if not proper:
                    ctk.msgbox.showwarning("Error", msg)
                    return
                self.shipping_data = [address_input.get(), city_input.get(), state_select.get(), zipcode_input.get()]
                shipping_window.destroy()
            
            # Address
            address_text = ctk.CTkLabel(shipping_window, text= "Address", text_color="#000", font=("Roboto", 16))
            address_text.grid(row=0, column=0, pady=(10, 0))
            address_input = ctk.CTkEntry(shipping_window)
            address_input.grid(row=0, column=1, sticky="ew", padx=10)
            # City
            city_text = ctk.CTkLabel(shipping_window, text= "City", text_color="#000", font=("Roboto", 16))
            city_text.grid(row=1, column=0, pady=(10, 0))
            city_input = ctk.CTkEntry(shipping_window)
            city_input.grid(row=1, column=1)
            # Zip Code
            zipcode_text = ctk.CTkLabel(shipping_window, text= "Zip Code", text_color="#000", font=("Roboto", 16))
            zipcode_text.grid(row=2, column=0, pady=(10, 0))
            zipcode_input = ctk.CTkEntry(shipping_window)
            zipcode_input.grid(row=2, column=1)
            # State
            state_text = ctk.CTkLabel(shipping_window, text= "State", text_color="#000", font=("Roboto", 16))
            state_text.grid(row=3, column=0)
            state_select = ctk.CTkEntry(shipping_window)
            state_select.grid(row=3, column=1, sticky="ew", padx=10)
            
            # Submit button
            submit_button = ctk.CTkButton(shipping_window, text="Submit", command=save_shipping_info, text_color="#000", font=("Roboto", 16))
            submit_button.grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')

        # Shipping Option checkbox
        shipping_text = ctk.CTkLabel(self, text="Shipping?", text_color="#000", font=("Roboto", 16))
        shipping_text.grid(row=row_offset, column=5)
        ship_var = ctk.BooleanVar()
        shipping_checkb = ctk.CTkCheckBox(self, variable=ship_var, text_color="#000", font=("Roboto", 16))
        shipping_checkb.grid(row=row_offset, column=6, sticky="ew", padx=10)
        
        # Bind the open_shipping_window function to the checkbox
        shipping_checkb.bind("<Button-1>", lambda event: open_shipping_window())

        row_offset += 1  # Increment row offset 

        # Divider
        divider = ctk.Separator(self, orient='horizontal')
        divider.grid(row=row_offset, column=1, columnspan=6, sticky='ew', pady=10)

        row_offset += 1  # Increment row offset 

        # Title for Vendors
        vendors_text = ctk.CTkLabel(self, text="Vendors",font=("Roboto", 16), text_color="#000")
        vendors_text.grid(row=row_offset, column=4, pady=(10, 0))
        # Radio Button for Vendors
        vendors = ctk.StringVar(self, "Vendors")
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
        typs = ctk.StringVar(self, "Type")
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
        divider = ctk.Separator(self, orient='horizontal')
        divider.grid(row=row_offset, column=0, columnspan=7, sticky='ew', pady=10)
        row_offset += 2  # Increment row offset

        # CX name inpput
        cx_name_title = ctk.CTkLabel(self, text="Name", text_color="#000", font=("Roboto", 16))
        cx_name_title.grid(row=row_offset, column=2)
        cx_name_input = ctk.CTkEntry(self)
        cx_name_input.grid(row=row_offset + 1, column=2, padx=10)

        # CX phone number input
        cx_phone_title = ctk.CTkLabel(self, text="Phone", text_color="#000", font=("Roboto", 16))
        cx_phone_title.grid(row=row_offset, column=4)
        cx_phone_input = ctk.CTkEntry(self)
        cx_phone_input.grid(row=row_offset + 1, column=4, padx=10)

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




class SO_App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Special Order")
        self.geometry("1200x680")
        self.configure(background="#350909")

        self.sidebar_menu = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_menu.grid(row=0, column=0, sticky='nsew', rowspan=8)
        self.sidebar_menu.grid_rowconfigure(4, weight=1)

        self.special_order_form = SO_Form(self)
        self.previous_orders = Prev_SO(self)
        self.ai_form = ai.DescriptionInputFrame(self)
        self.reconciliation_form = None

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
        for frame in [self.special_order_form, self.previous_orders, self.ai_form]:
            frame.grid_forget()

    def show_special_order_form(self):
        self.configure(background="#ffced0")
        self.hide_all_frames()
        self.special_order_form.grid(row=0, column=1, sticky='nsew')
        self.special_order_form_button["state"]="disabled"

    def show_previous_orders(self):
        self.hide_all_frames()
        self.previous_orders.grid(row=0, column=1, sticky='nsew')
        self.previous_orders_button["state"]="disabled"

    def show_ai_form(self):
        self.hide_all_frames()
        self.ai_form.grid(row=0, column=1, sticky='nsew')
        self.ai_form_button["state"]="disabled"

    def show_reconciliation_form(self):
        self.hide_all_frames(row=0, column=1, sticky='nsew')
        self.reconciliation_form.grid()
        self.reconciliation_form_button["state"]="disabled"

    def show_main_frame(self):
        self.hide_all_frames()
        # Show the main application frame
        self.previous_orders_button.grid()
        self.special_order_form_button.grid()



window = SO_App()
window.mainloop()