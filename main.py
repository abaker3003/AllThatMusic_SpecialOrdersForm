import tkinter as tk
from tkinter import ttk
'''from tkinter import *
from tkinter.ttk import *
from tkinter.tix import *'''
import tkinter.messagebox as msgbox
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
    self.header.grid(row=0,
                     column=1,
                     columnspan=2,
                     sticky='w',
                     pady=(10, 20),
                     padx=10)

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
      if not cx_phone_input.get().isdigit():
        errormsg += str(num_of_msgs) + ': Phone number must be numbers only.\n'
        proper = False
        num_of_msgs += 1
      if len(cx_phone_input.get()) != 10:
        errormsg += str(
            num_of_msgs) + ": Phone number must be exactly 10 digits long.\n"
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
      else:
        data.append("No")
        data.extend(["N/A"] * len(self.shipping_data))
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

    # Date
    date_text = ctk.CTkLabel(self,
                             text="Date: " + todays_date,
                             text_color="#FFFFFF",
                             font=("Roboto", 16))
    date_text.grid(row=row_offset, column=2, columnspan=1, pady=(10, 0))

    # Clerk name input
    clerk_text = ctk.CTkLabel(self,
                              text="Clerk",
                              text_color="#FFFFFF",
                              font=("Roboto", 16))
    clerk_text.grid(row=row_offset, column=3)
    clerk_input = ctk.CTkEntry(self)
    clerk_input.grid(row=row_offset, column=4, sticky="ew", padx=10)

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
    shipping_text.grid(row=row_offset, column=5)
    ship_var = ctk.BooleanVar(self)
    shipping_checkb = ctk.CTkCheckBox(self, variable=ship_var, text=None)
    shipping_checkb.grid(row=row_offset, column=6, sticky="ew", padx=10)

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
                                font=("Roboto", 20),
                                text_color="#FFFFFF")
    vendors_text.grid(row=0, column=1, pady=(10, 0), sticky='ew')
    # Radio Button for Vendors
    vendors = ctk.StringVar(self.vendors_buttons, "Vendors")
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
    self.type_buttons.grid(row=row_offset, column=3, columnspan=3, sticky='ew')
    # Title for Type
    type_text = ctk.CTkLabel(self.type_buttons,
                             text="Type",
                             font=("Roboto", 20),
                             text_color="#FFFFFF")
    type_text.grid(row=0, column=1, pady=(10, 0))

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
    cx_name_input = ctk.CTkEntry(self)
    cx_name_input.grid(row=row_offset + 1, column=2, padx=10)

    # CX phone number input
    cx_phone_title = ctk.CTkLabel(self,
                                  text="Phone",
                                  text_color="#FFFFFF",
                                  font=("Roboto", 16))
    cx_phone_title.grid(row=row_offset, column=4)
    cx_phone_input = ctk.CTkEntry(self)
    cx_phone_input.grid(row=row_offset + 1, column=4, padx=10)

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
                               text="Price",
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


class Prev_SO(ctk.CTkFrame):

  def __init__(self, *args, header_name="Previous Special Orders", **kwargs):
    super().__init__(*args, **kwargs)
    self.header_name = header_name
    self.header = ctk.CTkLabel(self, text=header_name, font=("Roboto", 20))
    self.header.grid(row=0, column=0, sticky='nsew', rowspan=8)

    # Load the Excel file into a pandas DataFrame
    self.excel_file = xl.open_excel_file('SO_Test.xlsx')
    self.df = self.excel_file.read_into_dataframe_SO()

    
    self.scrollbar_x = ttk.Scrollbar(self,
                                     orient='horizontal')
    self.scrollbar_x.grid(row=2, column=0, sticky='ew', padx=10, pady=(0, 10))

    # Create the Treeview
    self.tree = ttk.Treeview(self,
                             columns=list(self.df.columns),
                             show="headings",xscrollcommand=self.scrollbar_x.set)
    for column in self.df.columns:
      self.tree.heading(column, text=column)
      self.tree.column(column, width=100,
                       anchor='center')  
      # Adjust width and centering as needed
    self.tree.grid(row=1, column=0, sticky='nsew', padx=10, pady=5)

    self.scrollbar_x.config(command=self.tree.xview)

    # Add the data to the Treeview
    for _, row in self.df.iterrows():
      self.tree.insert('', 'end', values=list(row))

    # Configure the grid to expand the treeview with window resizing
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)

    # Create the Scrollbar
    self.scrollbar_y = ttk.Scrollbar(self,
                                     orient='vertical',
                                     command=self.tree.yview)
    self.scrollbar_y.grid(row=1, column=1, sticky='ns', padx=(0, 10), pady=5)
    self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)


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
    values = self.tree.item(item, 'values')


    # Create a dialog with entry fields for each column
    self.dialog = ctk.CTkToplevel(self)
    self.dialog.geometry("350x580")
    self.scroll_diag = ctk.CTkScrollableFrame(self.dialog, height=400, width=280)
    self.scroll_diag.grid(row=0, column=0, columnspan=4, padx=10, pady=10)


    self.dialog.title("Edit Order")
    self.entries = {}

    typ_values = ["CD", "DVD", "BLU-RAY", "LP", "OTHER"]
    vendors_values = ["AEC", "AMS", "AMA"]

    for i, column in enumerate(self.df.columns):
      ctk.CTkLabel(self.scroll_diag, text=column, font=("Arial", 10)).grid(row=i,
                                                                      column=0,
                                                                      padx=10,
                                                                      pady=5)

      if column == "VENDOR":
        entry = ctk.CTkOptionMenu(self.scroll_diag, values=vendors_values)
        entry.set(values[i])  # Set to current value or default one
        entry.grid(row=i, column=1, padx=10, pady=5)
      elif column == "TYPE":
        entry = ctk.CTkOptionMenu(self.scroll_diag, values=typ_values)
        entry.set(values[i])  # Set to current value or default one
        entry.grid(row=i, column=1, padx=10, pady=5)
      elif column == "SHIPPING?": 

        self.shipping_info_entries = ["ADDRESS", "CITY", "STATE", "ZIPCODE"]

        shipping_labels = []

        self.shipping_entries = []

        def show_shipping_info():
        
          for j, info in enumerate(self.shipping_info_entries):
            label = ctk.CTkLabel(self.scroll_diag, text=info, font=("Roboto", 12))
            label.grid(row=self.start_row_index + j, column=0, padx=10, pady=5)
            shipping_entry_val = ctk.StringVar(value=values[self.start_row_index + j])
            shipping_entry = ctk.CTkEntry(self.scroll_diag, textvariable=shipping_entry_val)
            shipping_entry.grid(row=self.start_row_index + j, column=1, padx=10, pady=5)
            self.shipping_entries.append(shipping_entry_val)
            shipping_labels.append(label)
            self.entries[info] = shipping_entry_val

        def hide_shipping_info():
          for shipping_widget in self.shipping_entries:
            shipping_widget.grid_remove()
          for shipping_label in shipping_labels:
            shipping_label.grid_remove()

        def on_shipping_option_changed(value):
          if value == "YES":
            show_shipping_info()
          else:
            hide_shipping_info()

        self.switch = ctk.StringVar(value=values[i])
        entry = ctk.CTkSwitch(self.scroll_diag, variable=self.switch, onvalue="YES", offvalue="NO")
        entry.grid(row=i, column=1, padx=10, pady=5)
        self.switch.trace_add("write", lambda *args: on_shipping_option_changed(self.switch.get()))
        self.entries[column] = self.switch

        # Start index for shipping info elements
        self.start_row_index = i + 1

        break

      else:
        entry = ctk.CTkEntry(self.scroll_diag)
        entry.insert(0, values[i])
        entry.grid(row=i, column=1, padx=10, pady=5)

      if column in set(["REF NUM", "DATE", "CLERK NAME"]):
        entry.configure(state='disabled')

      self.entries[column] = entry

    button_start_row_index = self.start_row_index

    print(self.entries)

    self.save_changes_button = ctk.CTkButton(
        self.dialog, text="Save", command=lambda: self.save(item, self.entries))
    self.save_changes_button.grid(row=button_start_row_index,
                                  column=0,
                                  columnspan=2,
                                  pady=20)

    self.cancel_changes_button = ctk.CTkButton(
        self.dialog, text="Cancel", command=self.dialog.destroy)
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
    print(self.df.columns)
    # Update the Treeview and the DataFrame with the new values
    new_values = [entries[column].get() for column in self.df.columns]    
    self.tree.item(item, values=new_values)

    # Assuming that 'I004' format means 'I' followed by an actual index number
    if item.startswith('I') and item[1:].isdigit():
      item_index = int(item[1:])
    else:
      # Handle the case where item does not follow the expected format
      raise ValueError(
          f"The item identifier {item} is not in the expected format.")

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


class SO_App(ctk.CTk):

  def __init__(self):
    super().__init__()
    self.title("Special Order")
    self.geometry("500x500")
    self.configure(background="#350909")

    self.sidebar_menu = ctk.CTkFrame(self, width=140, corner_radius=0)
    self.sidebar_menu.grid(row=0, column=0, sticky='nsew', rowspan=4)
    self.sidebar_menu.grid_rowconfigure(4, weight=1)

    self.special_order_form = SO_Form(self)
    self.previous_orders = Prev_SO(self)
    self.ai_form = ai.DescriptionInputFrame(self)
    self.reconciliation_form = None

    self.special_order_form_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Special Order Form",
        command=self.show_special_order_form,
        fg_color="#990000",
        border_color="red",
        font=("Arial", 30),
        text_color="#FFFFFF")

    self.previous_orders_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Previous Orders",
        command=self.show_previous_orders,
        fg_color="#990000",
        border_color="red",
        font=("Arial", 30),
        text_color="#FFFFFF")

    self.ai_form_button = ctk.CTkButton(self.sidebar_menu,
                                        text="AI Form",
                                        command=self.show_ai_form,
                                        fg_color="#990000",
                                        border_color="red",
                                        font=("Arial", 30),
                                        text_color="#FFFFFF")

    self.reconciliation_form_button = ctk.CTkButton(
        self.sidebar_menu,
        text="Reconciliation Form",
        command=self.show_reconciliation_form,
        fg_color="#990000",
        border_color="red",
        font=("Arial", 30),
        text_color="#FFFFFF")

    self.hide_all_frames()

    self.special_order_form_button.grid(row=0, column=0)
    self.previous_orders_button.grid(row=1, column=0)
    self.ai_form_button.grid(row=2, column=0)
    self.reconciliation_form_button.grid(row=3, column=0)

  def hide_all_frames(self):
    for frame in [self.special_order_form, self.previous_orders, self.ai_form]:
      frame.grid_forget()
    self.enable_buttons()

  def enable_buttons(self):
    for buttons in [
        self.special_order_form_button, self.previous_orders_button,
        self.ai_form_button, self.reconciliation_form_button
    ]:
      buttons.configure(state="normal")

  def show_special_order_form(self):
    self.geometry("1050x500")
    self.configure(background="#ffced0")
    self.hide_all_frames()
    self.special_order_form.grid(row=3, column=1, sticky='nsew')
    self.special_order_form_button.configure(state="disabled")

  def show_previous_orders(self):
    self.geometry("1200x500")
    self.hide_all_frames()
    self.previous_orders.grid(row=0, column=1, sticky='nsew')
    self.previous_orders_button.configure(state="disabled")

  def show_ai_form(self):
    self.hide_all_frames()
    self.geometry("1100x600")
    self.ai_form.grid(row=0, column=1, sticky='nsew')
    self.ai_form_button.configure(state="disabled")

  def show_reconciliation_form(self):
    self.hide_all_frames()
    self.reconciliation_form.grid(row=0, column=1, sticky='nsew')
    self.reconciliation_form_button.configure(state="disabled")

  def show_main_frame(self):
    self.hide_all_frames()
    self.geometry("500x500")
    # Show the main application frame
    self.enable_buttons()


window = SO_App()
window.mainloop()
