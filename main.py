import tkinter as tk
from tkinter import Scrollbar, ttk
import tkinter.messagebox as msgbox
from typing import Tuple
import customtkinter as ctk
from matplotlib import artist
import generators as gn
import xlfile as xl
from tkinter import Scrollbar
import re
import getpass

ctk.set_default_color_theme('C:/Users/abake/OneDrive/Documents/AllThatMusic_SpecialOrdersForm/red.json')

class Reconciliation(ctk.CTkFrame):
  
  def __init__(self, *args, header_name="Reconciliation Form", **kwargs):
    super().__init__(*args, **kwargs)
    self.header_name = header_name
    self.master.title(header_name)

    self.total = 0.0

    # --- > First Frame < --- #

    self.vendor_info = ctk.CTkFrame(self)
    self.vendor_info.grid(row=0, column=0, columnspan=4, rowspan=2, sticky='nsew', padx=10, pady=10)

    # Vendor Name
    vendor_name_label = ctk.CTkLabel(self.vendor_info, text="Vendor Name", font=("Roboto", 16))
    vendor_name_label.grid(row=0, column=0, padx=(10,0), pady=5)

    vendors = ["AEC", "AMS", "AMA", "OTHER"]
    self.vendor = ctk.StringVar(self.vendor_info)
    self.vendor_opt = ctk.CTkOptionMenu(self.vendor_info, values=vendors, variable=self.vendor, font=("Roboto", 16), width=80)
    self.vendor_opt.grid(row=0, column=1, pady=5)
    self.vendor.trace_add('write', self.toggle_vendor_entry)

    self.vend_name = ctk.CTkEntry(self.vendor_info, font=("Roboto", 16), width=100)


    # Packing Slip 
    pack_slip_label = ctk.CTkLabel(self.vendor_info, text="Packing Slip", font=("Roboto", 16))
    pack_slip_label.grid(row=1, column=0, padx=10, pady=5)
    pack_slip = ctk.CTkEntry(self.vendor_info, font=("Roboto", 16), width=100)
    pack_slip.grid(row=1, column=1, padx=10, pady=5)

    date_label = ctk.CTkLabel(self.vendor_info, text="Date", font=("Roboto", 16))
    date_label.grid(row=0, column=4, padx=10, pady=5)
    date = ctk.CTkEntry(self.vendor_info, font=("Roboto", 16))
    date.grid(row=0, column=5, padx=10, pady=5)

    # Received by
    received_by_label = ctk.CTkLabel(self.vendor_info, text="Received By", font=("Roboto", 16))
    received_by_label.grid(row=1, column=4, padx=10, pady=5)
    self.received_by = ctk.CTkEntry(self.vendor_info, font=("Roboto", 16))
    self.received_by.grid(row=1, column=5, padx=10, pady=5)


    # --- > Second Frame < --- #

    self.details = ctk.CTkFrame(self)
    self.details.grid(row=2, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
    
    # CDs
    cds_label = ctk.CTkLabel(self.details, text="10 - CDs", font=("Roboto", 16))
    cds_label.grid(row=0, column=0, padx=10, pady=5)
    self.cds = ctk.DoubleVar(self.details, value=0)
    cds_entry = ctk.CTkEntry(self.details, textvariable=self.cds, font=("Roboto", 16))
    cds_entry.grid(row=0, column=1, padx=10, pady=5)
    self.cds.trace_add('write', self.update_totals)

    # 180g
    one_eighty_label = ctk.CTkLabel(self.details, text="15 - 180g", font=("Roboto", 16))
    one_eighty_label.grid(row=1, column=0, padx=10, pady=5)
    self.one_eighty = ctk.DoubleVar(self.details, value=0)
    one_eighty_entry = ctk.CTkEntry(self.details, textvariable=self.one_eighty, font=("Roboto", 16))
    one_eighty_entry.grid(row=1, column=1, padx=10, pady=5)
    self.one_eighty.trace_add('write', self.update_totals)

    # Spanish CDs
    spanish_cds_label = ctk.CTkLabel(self.details, text="20 - Spanish CDs", font=("Roboto", 16))
    spanish_cds_label.grid(row=2, column=0, padx=10, pady=5)
    self.spanish_cds = ctk.DoubleVar(self.details, value=0)
    spanish_cds_entry = ctk.CTkEntry(self.details, textvariable=self.spanish_cds, font=("Roboto", 16))
    spanish_cds_entry.grid(row=2, column=1, padx=10, pady=5)
    self.spanish_cds.trace_add('write', self.update_totals)

    # Pre-Owned
    pre_owned_label = ctk.CTkLabel(self.details, text="30 - Pre-Owned", font=("Roboto", 16))
    pre_owned_label.grid(row=3, column=0, padx=10, pady=5)
    self.pre_owned = ctk.DoubleVar(self.details, value=0)
    pre_owned_entry = ctk.CTkEntry(self.details, textvariable=self.pre_owned, font=("Roboto", 16))
    pre_owned_entry.grid(row=3, column=1, padx=10, pady=5)
    self.pre_owned.trace_add('write', self.update_totals)

    # DVDs
    dvds_label = ctk.CTkLabel(self.details, text="40 - DVDs", font=("Roboto", 16))
    dvds_label.grid(row=0, column=3, padx=10, pady=5)
    self.dvds = ctk.DoubleVar(self.details, value=0)
    dvds_entry = ctk.CTkEntry(self.details, textvariable=self.dvds, font=("Roboto", 16))
    dvds_entry.grid(row=0, column=4, padx=10, pady=5)
    self.dvds.trace_add('write', self.update_totals)

    # Accessories 
    accessories_label = ctk.CTkLabel(self.details, text="50 - Accessories", font=("Roboto", 16))
    accessories_label.grid(row=1, column=3, padx=10, pady=5)
    self.accessories = ctk.DoubleVar(self.details, value=0)
    accessories_entry = ctk.CTkEntry(self.details, textvariable=self.accessories, font=("Roboto", 16))
    accessories_entry.grid(row=1, column=4, padx=10, pady=5)
    self.accessories.trace_add('write', self.update_totals)

    # Boutique
    boutique_label = ctk.CTkLabel(self.details, text="60 - Boutique", font=("Roboto", 16))
    boutique_label.grid(row=2, column=3, padx=10, pady=5)
    self.boutique = ctk.DoubleVar(self.details, value=0.0)
    boutique_entry = ctk.CTkEntry(self.details, textvariable=self.boutique, font=("Roboto", 16))
    boutique_entry.grid(row=2, column=4, padx=10, pady=5)
    self.boutique.trace_add('write', self.update_totals)

    # Posters
    posters_label = ctk.CTkLabel(self.details, text="65 - Posters", font=("Roboto", 16))
    posters_label.grid(row=3, column=3, padx=10, pady=5)
    self.posters = ctk.DoubleVar(self.details, value=0)
    posters_entry = ctk.CTkEntry(self.details, textvariable=self.posters, font=("Roboto", 16))
    posters_entry.grid(row=3, column=4, padx=10, pady=5)
    self.posters.trace_add('write', self.update_totals)
    
    
    # --- > Third Frame < --- #

    self.totals = ctk.CTkFrame(self)
    self.totals.grid(row=3, column=0, columnspan = 2, sticky='nsew', padx=10, pady=10)

    # Subtotal
    subtotal_label = ctk.CTkLabel(self.totals, text="Subtotal", font=("Roboto", 20))
    subtotal_label.grid(row=0, column=0, padx=10, pady=5)
    self.subtotal = ctk.CTkLabel(self.totals, text=str(self.total), font=("Roboto", 20))
    self.subtotal.grid(row=0, column=1, padx=10, pady=5)


    # Shipping
    shipping_label = ctk.CTkLabel(self.totals, text="Shipping", font=("Roboto", 20))
    shipping_label.grid(row=2, column=0, padx=10, pady=5)
    self.shipping = ctk.DoubleVar(self.totals, value=0.0)
    shipping_entry = ctk.CTkEntry(self.totals, textvariable=self.shipping, font=("Roboto", 20), justify='center', width=60)
    shipping_entry.grid(row=2, column=1, padx=10, pady=5)
    self.shipping.trace_add('write', self.update_totals)

    self.grand_total_amount = (self.total + self.shipping.get())

    # Total 
    grand_total_label = ctk.CTkLabel(self.totals, text="Total", font=("Roboto", 20))
    grand_total_label.grid(row=3, column=0, padx=10, pady=5)
    self.grand_total = ctk.CTkLabel(self.totals, text=str(self.grand_total_amount), font=("Roboto", 20))
    self.grand_total.grid(row=3, column=1, padx=10, pady=5)


    # --- > Fourth Frame < --- #

    # Paid by (ck # / cc checkbox options)
    self.payment = ctk.CTkFrame(self)
    self.payment.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)

    # -- Checkboxes -- #
    # Check
    self.ck = ctk.BooleanVar(self.payment, value=False)
    self.ck_checkbox = ctk.CTkCheckBox(self.payment, text="Check", variable=self.ck, font=("Roboto", 16))
    self.ck_checkbox.grid(row=0, column=0, padx=10, pady=5, sticky='ew')

    # Check Number Entry
    self.ck_number = ctk.IntVar(self.payment)
    self.ck_number_entry = ctk.CTkEntry(self.payment, width=100)

    # Credit Card
    self.cc = ctk.BooleanVar(self.payment, value=False)
    self.cc_checkbox = ctk.CTkCheckBox(self.payment, text="Credit Card", variable=self.cc, font=("Roboto", 16))
    self.cc_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

    def toggle_ck_number():
      if self.ck.get():
        self.ck_number_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
      else:
        self.ck_number_entry.grid_forget()

    self.ck_checkbox.bind("<Button-1>", lambda event: toggle_ck_number())

    # Collect On Delivery
    self.cod = ctk.BooleanVar(self.payment, value=False)
    self.cod_checkbox = ctk.CTkCheckBox(self.payment, text="COD", variable=self.cod, font=("Roboto", 16))
    self.cod_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

    # Open
    self.open = ctk.BooleanVar(self.payment, value=False)
    self.open_checkbox = ctk.CTkCheckBox(self.payment, text="Open", variable=self.open, font=("Roboto", 16))
    self.open_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky='ew')

    # Cash 
    self.cash = ctk.BooleanVar(self.payment, value=False)
    self.cash_checkbox = ctk.CTkCheckBox(self.payment, text="Cash", variable=self.cash, font=("Roboto", 16))
    self.cash_checkbox.grid(row=4, column=0, padx=10, pady=5, sticky='ew')


    # --- > Fifth Frame < --- #

    # Notes
    self.notes = ctk.CTkFrame(self)
    self.notes.grid(row=0, column=5, rowspan=4, sticky='nsew', padx=10, pady=10)
    self.note_label = ctk.CTkLabel(self.notes, text="Notes", font=("Roboto", 16))
    self.note_label.grid(row=0, column=0, padx=10, pady=5)
    self.note_text = ctk.CTkTextbox(self.notes, width=180, height=350, font=("Roboto", 15), wrap='word')
    self.note_text.grid(row=1, column=0, padx=10, pady=5)

    self.save = ctk.CTkButton(self.notes, text="Save", command=None, font=("Roboto", 16))
    self.save.grid(row=2, column=0, padx=10, pady=20, sticky='ew')

  def toggle_vendor_entry(self, *args):
      if self.vendor.get() == "OTHER":
        self.vend_name.grid(row=0, column=3, pady=5)
      else:
        self.vend_name.grid_forget()


  def update_totals(self, *args):
    self.total = 0.0
    self.total += float(self.cds.get())
    self.total += float(self.one_eighty.get())
    self.total += float(self.spanish_cds.get())
    self.total += float(self.dvds.get())
    self.total += float(self.accessories.get())
    self.total += float(self.boutique.get())
    self.total += float(self.posters.get())
    self.subtotal.configure(text = str(self.total))
    self.grand_total.configure(text = str(self.total  + self.shipping.get()))

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
    self.header.grid(row=0,
                     column=1,
                     columnspan=2,
                     sticky='w',
                     pady=(10, 20),
                     padx=10)
    
    # Date
    date_text = ctk.CTkLabel(self,
                             text="Date: " + todays_date,
                             text_color="#FFFFFF",
                             font=("Roboto", 16))
    date_text.grid(row=0, column=3, columnspan=1, pady=(10, 0))

    # Adding the current date and ticket number to data list
    data = [todays_date, ticket_num]

    # Checks if all input fields are filled
    def check_form_complete():
      # Check if all required entries have text
      if not cx_name_input.get() or not cx_phone_input.get(
      ) or not artist_input.get() or not title_input.get(
      ) or not deposit_input.get() or not price_input.get():
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
            errormsg += str(
                num_of_msgs) + ': Customer name must be all letters.\n'
            proper = False
            num_of_msgs += 1
            break
      elif not cx_name_input.get().isalpha():
        errormsg += str(num_of_msgs) + ': Customer name must be all letters.\n'
        proper = False
        num_of_msgs += 1
      if not re.match(r'^\d{10}$', re.sub(r'\D', '', cx_phone_input.get())):
        errormsg += str(num_of_msgs) + ': Phone number must be 10 digits'
        proper = False
        num_of_msgs += 1
      if not deposit_input.get().isdigit() and '.' not in deposit_input.get():
        errormsg += str(
            num_of_msgs
        ) + ": Deposit amount should not contain any other symbols except decimal.\n"
        proper = False
        num_of_msgs += 1
      if not price_input.get().isdigit() and '.' not in price_input.get():
        errormsg += str(
            num_of_msgs
        ) + ": Price amount should not contain any other symbols except decimal.\n"
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
      
      data.append("NO")

      data.append(cx_name_input.get())
      data.append(cx_phone_input.get())
      data.append(text_cx.get())
      data.append(call_cx.get())
      data.append(artist_input.get())
      data.append(title_input.get())
      data.append(float(deposit_input.get()))
      data.append(float(price_input.get()))
      data.append(" ")
      data.append(vendors.get())
      data.append(typs.get())
      data.append(self.username)
      if ship_var.get() == 1:
        data.append("SHIPPING")
        data.extend(self.shipping_data)
      else:
        data.append("PICKUP")
        data.extend(["N/A" for i in range(len(self.shipping_data))])
        print(data)
      gn.first_SO_of_day(xl_file, int(ticket_num[-3:]))
      xl_file.writeOnXL(data)
      xl_file.close_file()
      save_button.configure(text="Saved!")
      save_button.configure(state="disabled")
      back_button.configure(text="Back")

    def go_back():
      xl_file.close_file()
      self.master.show_main_frame()

    #--> DISPLAYED <--#

    row_offset = 1  # Initialize row offset for better readability

    # Clerk name input
    self.username = getpass.getuser()
    clerk_text = ctk.CTkLabel(self,
                              text="Clerk: ",
                              text_color="#FFFFFF",
                              font=("Roboto", 16))
    clerk_text.grid(row=row_offset, column=1,  padx=(20,5), sticky='e')
    clerk_input = ctk.CTkLabel(self, text=self.username, font=("Roboto", 16, "bold"))
    clerk_input.grid(row=row_offset, column=2, sticky="w", padx=(5,20))

    self.shipping_data = []

    def open_shipping_window():
      self.shipping_window = ctk.CTkToplevel(self)
      self.shipping_window.title("Shipping Information")

      def check_shipping_info_complete():
        if not address_input.get() or not city_input.get(
        ) or not zipcode_input.get() or not state_select.get():
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
          errormsg += str(
              num_of_msgs) + ": Zip code must be exactly 5 digits long.\n"
          proper = False
          num_of_msgs += 1
        if not state_select.get():
          errormsg += str(num_of_msgs) + ': State cannot be empty.\n'
          proper = False
          num_of_msgs += 1
        return proper, errormsg

      def save_shipping_info():
        if not check_shipping_info_complete():
          msgbox.showerror("Error", "Please fill out the entire form.")
          return
        proper, msg = check_proper_info()
        if not proper:
          msgbox.showwarning("Error", msg)
          return
        self.shipping_data = [
            address_input.get(),
            city_input.get(),
            state_select.get(),
            zipcode_input.get()
        ]
        self.shipping_window.destroy()

      # Address
      address_text = ctk.CTkLabel(self.shipping_window,
                                  text="Address",
                                  text_color="#FFFFFF",
                                  font=("Roboto", 16))
      address_text.grid(row=0, column=0, pady=(10, 0))
      address_input = ctk.CTkEntry(self.shipping_window)
      address_input.grid(row=0, column=1, sticky="ew", padx=10)
      # City
      city_text = ctk.CTkLabel(self.shipping_window,
                               text="City",
                               text_color="#FFFFFF",
                               font=("Roboto", 16))
      city_text.grid(row=1, column=0, pady=(10, 0))
      city_input = ctk.CTkEntry(self.shipping_window)
      city_input.grid(row=1, column=1)
      # Zip Code
      zipcode_text = ctk.CTkLabel(self.shipping_window,
                                  text="Zip Code",
                                  text_color="#FFFFFF",
                                  font=("Roboto", 16))
      zipcode_text.grid(row=2, column=0, pady=(10, 0))
      zipcode_input = ctk.CTkEntry(self.shipping_window)
      zipcode_input.grid(row=2, column=1)
      # State
      state_text = ctk.CTkLabel(self.shipping_window,
                                text="State",
                                text_color="#FFFFFF",
                                font=("Roboto", 16))
      state_text.grid(row=3, column=0)
      state_select = ctk.CTkEntry(self.shipping_window)
      state_select.grid(row=3, column=1, sticky="ew", padx=10)

      # Submit button
      submit_button = ctk.CTkButton(self.shipping_window,
                                    text="Submit",
                                    command=save_shipping_info,
                                    text_color="#FFFFFF",
                                    font=("Roboto", 16))
      submit_button.grid(row=4, column=0, columnspan=2, pady=20, sticky='ew')

    # Shipping Option checkbox
    shipping_text = ctk.CTkLabel(self,
                                 text="Shipping?",
                                 text_color="#FFFFFF",
                                 font=("Roboto", 16))
    shipping_text.grid(row=row_offset, column=4)
    ship_var = ctk.BooleanVar(self)
    shipping_checkb = ctk.CTkCheckBox(self, variable=ship_var, text=None, onvalue=1, offvalue=0)
    shipping_checkb.grid(row=row_offset, column=5, sticky="ew", padx=10)

    # Bind the open_shipping_window function to the checkbox
    def toggle_shipping_window():
      if ship_var.get():
        open_shipping_window()
      else:
        if hasattr(self, 'shipping_window') and self.shipping_window:
          self.shipping_window.destroy()
          self.shipping_window = None

    self.shipping_window = None
    shipping_checkb.bind("<Button-1>", lambda event: toggle_shipping_window())

    row_offset += 1  # Increment row offset

    # Divider
    #divider = ttk.Separator(self, orient='horizontal')
    divider = ctk.CTkFrame(self, height=2, fg_color="gray")
    divider.grid(row=row_offset, column=1, columnspan=6, sticky='ew', pady=10)

    row_offset += 1  # Increment row offset

    self.vendors_buttons = ctk.CTkFrame(self)
    self.vendors_buttons.grid(row=row_offset,
                              column=1,
                              columnspan=2,
                              sticky='e',
                              pady=10,
                              padx=40)
    # Title for Vendors
    vendors_text = ctk.CTkLabel(self.vendors_buttons,
                                text="Vendors",
                                font=("Arial Black", 20),
                                text_color="#FFFFFF")
    vendors_text.grid(row=0, column=1, pady=(0, 10), sticky='new')
    # Radio Button for Vendors
    vendors = ctk.StringVar(self.vendors_buttons)
    vendors_values = ["AEC", "AMS", "AMA"]

    # Button positioning based on amount of options
    for i, vendor in enumerate(vendors_values):
      rdio_opt = ctk.CTkRadioButton(self.vendors_buttons,
                                    text=vendor,
                                    variable=vendors,
                                    value=vendor,
                                    text_color="#FFFFFF",
                                    font=("Roboto", 16))
      rdio_opt.grid(row=1, column=i, sticky='ew')

    self.type_buttons = ctk.CTkFrame(self)
    self.type_buttons.grid(row=row_offset, column=3, columnspan=3)
    # Title for Type
    type_text = ctk.CTkLabel(self.type_buttons,
                             text="Type",
                             font=("Arial Black", 20),
                             text_color="#FFFFFF")
    type_text.grid(row=0, column=1, pady=(0, 10), sticky='new')

    # Radio Button for Type
    typs = ctk.StringVar(self.type_buttons, "Type")
    typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]

    # Button positioning based on amount of options
    for i, typ in enumerate(typ_values):
      if i < 3:
        rdio_typ = ctk.CTkRadioButton(self.type_buttons,
                                      text=typ,
                                      variable=typs,
                                      value=typ,
                                      text_color="#FFFFFF",
                                      font=("Roboto", 16))
        rdio_typ.grid(row=1, column=i, sticky='e')
      else:
        rdio_typ = ctk.CTkRadioButton(self.type_buttons,
                                      text=typ,
                                      variable=typs,
                                      value=typ,
                                      text_color="#FFFFFF",
                                      font=("Roboto", 16))
        rdio_typ.grid(row=2, column=i - 3, sticky='e')

    row_offset += 2  # Increment row offset

    # Divider
    #divider = ttk.Separator(self, orient='horizontal')
    divider = ctk.CTkFrame(self, height=2, fg_color="gray")
    divider.grid(row=row_offset, column=0, columnspan=7, sticky='ew', pady=10)
    row_offset += 2  # Increment row offset

    # CX name inpput
    cx_name_title = ctk.CTkLabel(self,
                                 text="Name",
                                 text_color="#FFFFFF",
                                 font=("Roboto", 16))
    cx_name_title.grid(row=row_offset, column=2)
    cx_name_input = ctk.CTkEntry(self, placeholder_text="No numbers")
    cx_name_input.grid(row=row_offset + 1, column=2, padx=10)

    # CX phone number input
    cx_phone_title = ctk.CTkLabel(self,
                                  text="Phone",
                                  text_color="#FFFFFF",
                                  font=("Roboto", 16))
    cx_phone_title.grid(row=row_offset, column=4)

    text_cx = ctk.CTkCheckBox(self, text="Text?", text_color="#FFFFFF", onvalue="YES", offvalue="NO")
    text_cx.grid(row=row_offset, column=5, padx=10)

    cx_phone_input = ctk.CTkEntry(self, placeholder_text="10 digits, no symbols")
    cx_phone_input.grid(row=row_offset + 1, column=4, padx=10)

    call_cx = ctk.CTkCheckBox(self, text="Call?", text_color="#FFFFFF", onvalue="YES", offvalue="NO")
    call_cx.grid(row=row_offset + 1, column=5, padx=10)

    def format_phone_number(event):
        phone_number = cx_phone_input.get()
        
        # Add error handling for empty or invalid input
        if not phone_number or not re.match(r'^\d{10}$', phone_number):
            cx_phone_input.delete(0, "end")
            cx_phone_input.insert(0, phone_number)
            return
        
        formatted_number = "({}){}-{}".format(phone_number[:3], phone_number[3:6], phone_number[6:])
        cx_phone_input.delete(0, "end")
        cx_phone_input.insert(0, formatted_number)

    # Bind the function to the KeyRelease event
    cx_phone_input.bind("<KeyRelease>", format_phone_number)

    row_offset += 2  # Increment row offset

    # Artist input
    artist_title = ctk.CTkLabel(self,
                                text="Artist",
                                text_color="#FFFFFF",
                                font=("Roboto", 16))
    artist_title.grid(row=row_offset, column=2)
    artist_input = ctk.CTkEntry(self)
    artist_input.grid(row=row_offset + 1, column=2, padx=10)

    # Title input
    title_title = ctk.CTkLabel(self,
                               text="Title",
                               text_color="#FFFFFF",
                               font=("Roboto", 16))
    title_title.grid(row=row_offset, column=4)
    title_input = ctk.CTkEntry(self)
    title_input.grid(row=row_offset + 1, column=4, padx=10)

    row_offset += 2  # Increment row offset

    # Deposit input
    deposit_title = ctk.CTkLabel(self,
                                 text="Deposit",
                                 text_color="#FFFFFF",
                                 font=("Roboto", 16))
    deposit_title.grid(row=row_offset, column=2)
    deposit_input = ctk.CTkEntry(self)
    deposit_input.grid(row=row_offset + 1, column=2, padx=10)

    # Price input
    price_title = ctk.CTkLabel(self,
                               text="Retail Price",
                               text_color="#FFFFFF",
                               font=("Roboto", 16))
    price_title.grid(row=row_offset, column=4)
    price_input = ctk.CTkEntry(self)
    price_input.grid(row=row_offset + 1, column=4, padx=10)

    row_offset += 2  # Increment row offset

    save_button = ctk.CTkButton(self,
                                text="Save",
                                command=save_checkbox_value,
                                text_color="#FFFFFF",
                                font=("Roboto", 16))
    save_button.grid(row=row_offset, column=2, pady=20)

    back_button = ctk.CTkButton(self,
                                text="Cancel",
                                command=go_back,
                                text_color="#FFFFFF",
                                font=("Roboto", 16))
    back_button.grid(row=row_offset, column=4, pady=20)

class CX_Call_Frame(ctk.CTkFrame):

  def __init__(self, *args, header_name="Customer Call", **kwargs):
    super().__init__(*args, **kwargs)

    self.header = ctk.CTkFrame(self)
    self.header.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

    date = gn.get_todays_date()
    user = getpass.getuser()

    date_label = ctk.CTkLabel(self.header, text="Date: " + date, font=("Roboto", 16))
    date_label.grid(row=0, column=0, pady=5, padx=(5, 20))
    clerk_label = ctk.CTkLabel(self.header, text="Clerk: " + user, font=("Roboto", 16))
    clerk_label.grid(row=0, column=3, pady=5, padx=(20,5))

    # search method for finding customer

    self.search_frame = ctk.CTkFrame(self)
    self.search_frame.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

    self.results_frame = ctk.CTkFrame(self)
    self.results_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

    search_methods = ["Phone Number", "Name", "Ticket Number"]
    self.input = ctk.CTkEntry(self.search_frame, font=("Roboto", 16))
    


    self.search_method_opt = ctk.StringVar(self.search_frame)
    for i, method in enumerate(search_methods):
      self.search_method_opt.set(search_methods[0])  # Set default value
      search_method_opt = ctk.CTkRadioButton(self.search_frame, text=method, value=method, font=("Roboto", 16), variable=self.search_method_opt)
      search_method_opt.grid(row=1, column=i, padx=10, pady=5)

    self.input.grid(row=2, column=1, padx=10, pady=5)
    #self.show_uncompleted_orders = ctk.BooleanVar(self.search_frame)
    show_uncompleted_orders = ctk.CTkCheckBox(self.search_frame, text="Only show uncompleted orders", font=("Roboto", 14), onvalue=True, offvalue=False)
    show_uncompleted_orders.grid(row=2, column=2, padx=10, pady=5)

    self.search_button = ctk.CTkButton(self.search_frame, text="Search", command=lambda: self.search(self.input.get(), self.search_method_opt.get(), show_uncompleted_orders.get()), font=("Roboto", 16))
    self.search_button.grid(row=4, column=1, padx=10, pady=20)

    

  def phone(self):
    phone_label = ctk.CTkLabel(self, text="Phone Number", font=("Roboto", 16))
    phone_label.grid(row=0, column=0, padx=10, pady=5)
    phone = ctk.CTkEntry(self, placeholder_text="10 digits, no symbols")
    phone.grid(row=1, column=0, padx=10)

    def format_phone_number(event):
        phone_number = phone.get()
        
        # Add error handling for empty or invalid input
        if not phone_number or not re.match(r'^\d{10}$', phone_number):
            phone.delete(0, "end")
            phone.insert(0, phone_number)
            return
        
        formatted_number = "({}){}-{}".format(phone_number[:3], phone_number[3:6], phone_number[6:])
        phone.delete(0, "end")
        phone.insert(0, formatted_number)

    # Bind the function to the KeyRelease event
    phone.bind("<KeyRelease>", format_phone_number)

    self.phone = phone

  def search(self, data, type, uncompleted):
    if type == "Phone Number":
      data = re.sub(r'\D', '', data)
      data = "({}){}-{}".format(data[:3], data[3:6], data[6:])
      return self.search_data(phone=data, uncompleted = uncompleted)
    elif data[:2] == 'SO' and data[2:].isdigit():
      return self.search_data(ticket=data, uncompleted = uncompleted)
    elif data[0].isalpha():
      return self.search_data(name=data, uncompleted = uncompleted)
    else:
      print("Invalid input. Please try again.")


  def search_data(self, phone=None, name=None, ticket=None, uncompleted=None):
    self.df = xl.open_excel_file('SO_Test.xlsx').read_into_dataframe_SO()
    print(uncompleted)
    if phone:
      matching_rows = self.df[self.df['PHONE'] == phone]
      if uncompleted:
        matching_rows = matching_rows[matching_rows['COMPLETED'] == 'NO']
      self.selection(matching_rows)
    elif name:
      matching_rows = self.df[self.df['CX NAME'] == name]
      if uncompleted:
        matching_rows = matching_rows[matching_rows['COMPLETED'] == 'NO']
      self.selection(matching_rows)
    elif ticket:
      matching_rows = self.df[self.df['REF NUM'] == ticket]
      if uncompleted:
        matching_rows = matching_rows[matching_rows['COMPLETED'] == 'NO']
      self.selection(matching_rows)

  
  def selection(self, matching_rows):

    self.final_result = ctk.StringVar(self.results_frame)

    i = 0
    
    for idx, row in matching_rows.iterrows():
      print(idx)
      display__text = row['REF NUM'] + " : " + row['CX NAME'] + " - " + row['PHONE'] + "\t"
      if row['COMPLETED'] == 'NO':
        display__text += " - UNCOMPLETED"
      else:
        display__text += " - COMPLETED"
      result = ctk.CTkRadioButton(self.results_frame, text=display__text, value=idx, font=("Roboto", 16), variable=self.final_result)
      result.grid(row=i, column=0, padx=10, pady=10)
      i += 1

class Prev_SO(ctk.CTkFrame):

  def __init__(self, *args, header_name="Previous Special Orders", **kwargs):
    super().__init__(*args, **kwargs)
    self.header_name = header_name
    self.header = ctk.CTkLabel(self, text=header_name, font=("Roboto", 20))
    self.header.grid(row=0, column=0, sticky='nsew', rowspan=8)

    # Load the Excel file into a pandas DataFrame
    self.excel_file = xl.open_excel_file('SO_Test.xlsx')
    self.df = self.excel_file.read_into_dataframe_SO()

    self.tree_frame = ctk.CTkScrollableFrame(self,
                                             width=700,
                                             height=300,
                                             orientation='horizontal')

    self.tree_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

    style = ttk.Style()
    style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
    style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
    style.map("mystyle.Treeview", background=[('selected', 'blue')], foreground=[('selected', 'white')])

    # Create the Treeview
    self.tree = ttk.Treeview(self.tree_frame,
                             columns=list(self.df.columns),
                             show="headings", height=20, style="mystyle.Treeview")
    
    self.tree.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)

    for column in self.df.columns:
      self.tree.heading(column, text=column)
      self.tree.column(column, width=100, anchor='center')

    # Add the data to the Treeview
    for i, row in self.df.iterrows():
      self.tree.insert('', "end", values=list(row), iid=i)

    # Configure the grid to expand the treeview with window resizing
    self.tree.grid_columnconfigure(0, weight=1)
    self.tree.grid_rowconfigure(0, weight=1)

    # Back Button with CTk Improvement
    self.back_button = ctk.CTkButton(self,
                                     text="Back",
                                     command=self.master.show_main_frame,
                                     text_color="#FFFFFF")
    self.back_button.grid(row=3, column=0, padx=10, pady=20, sticky='w')

    # Bind the double-click event
    self.tree.bind('<Double-1>', self.on_double_click)

    self.dialog = None
    self.save_changes_button = None

  def on_double_click(self, event):
    # Get the selected item
    item = self.tree.selection()[0]
    print(item)
    values = self.tree.item(item, 'values')

    # Create a dialog with entry fields for each column
    self.dialog = ctk.CTkToplevel(self)
    self.dialog.geometry("350x580")
    self.scroll_diag = ctk.CTkScrollableFrame(self.dialog,
                                              height=400,
                                              width=280)
    self.scroll_diag.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    self.dialog.title("Edit Order")
    self.entry_keys = [column for column in self.df.columns]
    self.entries = {cul: "" for cul in self.entry_keys}

    typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
    vendors_values = ["AEC", "AMS", "AMA"]

    for i, column in enumerate(self.df.columns):
      ctk.CTkLabel(self.scroll_diag, text=column,
                   font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5)

      if column == "VENDOR":
        entry = ctk.CTkOptionMenu(self.scroll_diag, values=vendors_values)
        entry.set(values[i])  # Set to current value or default one
        entry.grid(row=i, column=1, padx=10, pady=5)
      elif column == "TEXT?" or column == "CALL?":
        label = ctk.CTkLabel(self.scroll_diag, text=column)
        label.grid(row=i, column=0, padx=10, pady=5)
        self.switch = ctk.StringVar(value=values[i])
        entry = ctk.CTkCheckBox(self.scroll_diag,
                              variable=self.switch,
                              onvalue="YES",
                              offvalue="NO", text="").grid(row=i, column=1, padx=10, pady=5)
        self.entries[column] = self.switch
        continue
      elif column == "COMPLETED":
        stat = ctk.CTkLabel(self.scroll_diag, text="Order Status: ")
        stat.grid(row=i, column=0, padx=10, pady=5)
        label = ctk.CTkLabel(self.scroll_diag, font=("Arial", 10, "bold"))
        if values[i] == "NO":
          label.configure(text="Uncompleted")
        else:
          label.configure(text="Completed")
        label.grid(row=i, column=1, padx=10, pady=5)
        continue
      elif column == "DEPOSIT" or column == "RETAIL":
        entry = ctk.DoubleVar(value=values[i])
        entry_num = ctk.CTkEntry(self.scroll_diag)
        entry_num.insert(0, values[i])  # Set to current value or default one
        entry_num.grid(row=i, column=1, padx=10, pady=5)
      elif column == "TEXT?" or column == "CALL?":
        self.switch = ctk.StringVar(value=values[i])
        entry = ctk.CTkSwitch(self.scroll_diag,
                              variable=self.switch,
                              onvalue="YES",
                              offvalue="NO")
        self.entries[column] = self.switch
        continue
      elif column == "TYPE":
        entry = ctk.CTkOptionMenu(self.scroll_diag, values=typ_values)
        entry.set(values[i])  # Set to current value or default one
        entry.grid(row=i, column=1, padx=10, pady=5)
      elif column == "SHIPPING?":

        self.shipping_info_entries = ["ADDRESS", "CITY", "STATE", "ZIPCODE"]

        shipping_labels = []

        self.shipping_entries = []

        self.start_row_index = i + 1

        def show_shipping_info():

          for j, info in enumerate(self.shipping_info_entries):
            label = ctk.CTkLabel(self.scroll_diag,
                                 text=info,
                                 font=("Roboto", 12))
            label.grid(row=self.start_row_index + j, column=0, padx=10, pady=5)
            shipping_entry_val = ctk.StringVar(
                value=values[self.start_row_index + j])
            shipping_entry = ctk.CTkEntry(self.scroll_diag,
                                          textvariable=shipping_entry_val)
            shipping_entry.grid(row=self.start_row_index + j,
                                column=1,
                                padx=10,
                                pady=5)
            self.shipping_entries.append(shipping_entry_val)
            shipping_labels.append(label)
            self.entries[info] = shipping_entry_val

        def hide_shipping_info():
          for shipping_widget in self.shipping_entries:
            shipping_widget.grid_remove()
          for shipping_label in shipping_labels:
            shipping_label.grid_remove()

        def on_shipping_option_changed(value):
          if value == "SHIPPING":
            show_shipping_info()
          else:
            hide_shipping_info()

        self.switch = ctk.StringVar(value=values[i])
        entry = ctk.CTkSwitch(self.scroll_diag,
                              variable=self.switch,
                              onvalue="SHIPPING",
                              offvalue="PICKUP")
        if values[i] == "SHIPPING":
          entry._check_state = True
          show_shipping_info()
        entry.grid(row=i, column=1, padx=10, pady=5)
        self.switch.trace_add(
            "write",
            lambda *args: on_shipping_option_changed(self.switch.get()))
        self.entries[column] = self.switch
        break

      else:
        entry = ctk.CTkEntry(self.scroll_diag)
        entry.insert(0, values[i])
        entry.grid(row=i, column=1, padx=10, pady=5)

      if column in set(["REF NUM", "DATE", "CLERK NAME"]):
        entry.configure(state='disabled')

      self.entries[column] = entry

    button_start_row_index = self.start_row_index

    self.save_changes_button = ctk.CTkButton(
        self.dialog,
        text="Save",
        command=lambda: self.save(item, self.entries))
    self.save_changes_button.grid(row=button_start_row_index,
                                  column=0,
                                  columnspan=2,
                                  pady=20)

    self.cancel_changes_button = ctk.CTkButton(self.dialog,
                                               text="Cancel",
                                               command=self.dialog.destroy)
    self.cancel_changes_button.grid(row=button_start_row_index + 1,
                                    column=0,
                                    columnspan=2,
                                    pady=20)

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
    new_values = [entries[column].get() if not isinstance(entries[column], str) else entries[column] for column in self.df.columns]
    self.tree.item(item, values=new_values)

    item_index = int(item) + 1

    print("Item index:", item_index)

    for column, new_value in zip(self.df.columns, new_values):
      self.df.at[item_index,
                 column] = new_value  # Make sure to use at[item_index, column]

    # Write the DataFrame back to the Excel file
    self.excel_file.update_excel(
        item_index + 1, new_values)  # Add 1 if necessary for Excel indexing

    self.save_changes_button.configure(text="Saved!", state="DISABLED")
    self.cancel_changes_button.configure(text="Back")

    # Destroy the dialog
    self.dialog.destroy()
    self.dialog = None

  def update_treeview(self):
    # Clear the Treeview
    for item in self.tree.get_children():
      self.tree.delete(item)
    # Reload the data
    self.df = self.excel_file.read_into_dataframe_SO()
    # Repopulate the Treeview with the updated data
    for i, row in self.df.iterrows():
      self.tree.insert('', "end", values=list(row), iid=i)

class SO_App(ctk.CTk):

  def __init__(self):
    super().__init__()
    self.title("Special Order")
    self.geometry("270x400")
    self.configure(background="#350909")

    self.sidebar_menu = ctk.CTkFrame(self, width=140, corner_radius=5)
    self.sidebar_menu.grid(row=0, column=0, sticky='nsew', rowspan=4, padx=10, pady=20)
    self.sidebar_menu.grid_rowconfigure(4, weight=1)

    self.special_order_form = SO_Form(self)
    self.cx_call = CX_Call_Frame(self)
    self.previous_orders = Prev_SO(self)
    self.ai_form = None
    self.reconciliation_form = Reconciliation(self)

    button_config = {
        "font": ("Arial", 30),
        "text_color": "#FFFFFF",
        "corner_radius": 10,
    }

    self.special_order_form_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Special Order",
        command=self.show_special_order_form,
        **button_config)
    
    self.cx_call_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Customer Call",
        command=self.show_cx_call,
        **button_config)

    self.previous_orders_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Previous Orders",
        command=self.show_previous_orders,
        **button_config)

    self.reconciliation_form_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Reconciliation",
        command=self.show_reconciliation_form,
        **button_config)

    self.hide_all_frames()

    self.special_order_form_button.grid(row=0, column=0, pady=25)
    self.cx_call_button.grid(row=1, column=0, pady=25)
    self.previous_orders_button.grid(row=2, column=0, pady=25)
    self.reconciliation_form_button.grid(row=3, column=0, pady=25)

  def hide_all_frames(self):
    for frame in [self.special_order_form, self.cx_call, self.previous_orders, self.reconciliation_form]:
      frame.grid_forget()
    self.enable_buttons()

  def enable_buttons(self):
    for buttons in [
        self.special_order_form_button, self.cx_call_button,  self.previous_orders_button, self.reconciliation_form_button
    ]:
      buttons.configure(state="normal")
      buttons.configure(fg_color="#d31313")

  def show_special_order_form(self):
    self.special_order_form = SO_Form(self)
    self.title("New Special Order")
    self.geometry("1065x460")
    self.hide_all_frames()
    self.special_order_form.grid(row=0, column=1, sticky='nsew')
    self.special_order_form_button.configure(fg_color="#000000")
    self.special_order_form_button.configure(state="disabled")

  def show_cx_call(self):
    self.geometry("1015x400")
    self.title("Customer Call")
    self.hide_all_frames()
    self.cx_call.grid(row=0, column=1, sticky='nsew')
    self.cx_call_button.configure(fg_color="#000000")
    self.cx_call_button.configure(state="disabled")

  def show_previous_orders(self):
    self.previous_orders.update_treeview()
    self.geometry("1015x400")
    self.title("Special Orders")
    self.hide_all_frames()
    self.previous_orders.grid(row=0, column=1, sticky='nsew')
    self.previous_orders_button.configure(fg_color="#000000")
    self.previous_orders_button.configure(state="disabled")

  def show_reconciliation_form(self):
    self.hide_all_frames()
    self.geometry("1100x500")
    self.title("Reconciliation Form")
    self.reconciliation_form.grid(row=0, column=1, sticky='nsew')
    self.reconciliation_form_button.configure(fg_color="#000000")
    self.reconciliation_form_button.configure(state="disabled")

  def show_main_frame(self):
    self.hide_all_frames()
    self.geometry("270x300")
    self.title("Special Order")
    # Show the main application frame
    self.enable_buttons()


window = SO_App()
window.mainloop()