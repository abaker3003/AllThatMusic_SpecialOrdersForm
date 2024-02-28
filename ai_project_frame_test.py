import torch
import torch.nn as nn
import torch.optim as optim
import xlfile as xl
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import threading
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI
import requests
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import CTkScrollableDropdown
import tkinter.messagebox as msgbox
from matplotlib import artist
import os
import dll as dll


class Condition(ctk.CTkFrame):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    conditions_list = [
        "Good", "Very Good", "Fairly Good", "Fair", "New", "Poor"
    ]
    self.condition = StringVar()

    condition_label = ctk.CTkLabel(self, text="Condition", font=("Helvetica", 18))
    condition_label.grid(row=0, column=0, columnspan=6, pady=10, sticky='ew')

    for i, cond in enumerate(conditions_list):
      cond_opt = ctk.CTkRadioButton(self,
                                    text=cond,
                                    variable=self.condition,
                                    value=cond)
      cond_opt.grid(row=1, column=i, padx=20, pady=20)

  def get_condition(self):
    return self.condition.get()


class Damage_Selection_Jacket(ctk.CTkFrame):

  def __init__(self, *args, header_name="Jacket Damages", **kwargs):
    super().__init__(*args, **kwargs)
    self.header_label = ctk.CTkLabel(self, text=header_name, font=("Helvetica", 18))
    self.header_label.grid(row=0, column=0, columnspan=6, sticky='ew')
    self.options = [
        "traces", "handling traces", "hairline", "hairlines", "sleeve dust",
        "sleeve rubs", "scuffings", "scuffs", "markings", "marks",
        "blemishing", "blemishes", "prints", "spindle marks", "ring wear",
        "corner wear"
    ]
    self.second_options = [
        "subtle", "faint", "barely-visible", "light", "minor", "occassional",
        "stray", "scattered", "mild", "moderate", "typical", "pronounced",
        "considerable", "severe"
    ]

    self.selections = {}
    self.is_option_selected = False
    self.main_func()

  def main_func(self):
    self.box_var = ctk.StringVar()
    self.box_option = ctk.CTkComboBox(self,
                                      variable=self.box_var,
                                      state="readonly")
    self.box_option_scroll = CTkScrollableDropdown.CTkScrollableDropdown(
        attach=self.box_option, values=self.options)
    self.box_option.grid(row=1,
                         column=0,
                         columnspan=2,
                         sticky='w',
                         pady=(10, 20),
                         padx=10)

    self.box_var2 = ctk.StringVar()
    self.box_option2 = ctk.CTkComboBox(self,
                                       variable=self.box_var2,
                                       state="readonly")
    self.box_option2_scroll = CTkScrollableDropdown.CTkScrollableDropdown(
        attach=self.box_option2, values=self.second_options)
    self.box_option2.grid(row=1,
                          column=2,
                          columnspan=2,
                          sticky='w',
                          pady=(10, 20),
                          padx=10)

    self.display_box = ctk.CTkFrame(self, height=100, width=300)
    self.display_box.grid(row=1,
                          column=4,
                          rowspan=4,
                          sticky='w',
                          pady=(10, 20),
                          padx=10)

    self.tree = ttk.Treeview(self.display_box,
                             columns=('Damage', 'Severity'),
                             show='headings',
                             height=8)
    self.tree.heading('Damage', text='Damage')
    self.tree.heading('Severity', text='Severity')

    self.add_btn = ctk.CTkButton(self, text="Add", command=self.box_selected)
    self.add_btn.grid(row=3, column=0, columnspan=2, sticky='e', padx=10)

    self.tree.grid(row=0,
                   column=0,
                   columnspan=2,
                   sticky='w',
                   pady=(10, 20),
                   padx=10)

    self.tree.bind('<<TreeviewSelect>>', self.on_select)

  def box_selected(self):
    self.selections[self.box_var.get()] = self.box_var2.get()
    self.tree.insert('',
                     'end',
                     values=(self.box_var.get(), self.box_var2.get()))
    idx = self.options.index(self.box_var.get())
    self.options.pop(idx)
    self.box_option_scroll.configure(values=self.options)
    self.box_var.set("")
    self.box_var2.set("")

  def close_dialog_and_reset(self):
    self.edit.destroy()
    self.delete.destroy()
    self.add_btn.configure(state="normal")
    self.edit = None
    self.delete = None
    self.is_option_selected = True

  def close_dialog(self):
    self.close_dialog_and_reset()

  def edit_option(self):

    def done():
      self.confirm_edit.destroy()
      self.confirm_edit = None
      self.dialog.destroy()
      self.is_option_selected = True
      self.close_dialog()

    def confirm_or_cancel():
      self.selections[option1] = self.box_option2_edit_val.get()
      tree_item = self.tree.selection()[0]
      self.tree.delete(tree_item)
      self.tree.unbind('<<TreeviewSelect>>')
      self.tree.insert('',
                       'end',
                       values=(option1, self.box_option2_edit_val.get()))
      self.tree.bind('<<TreeviewSelect>>', self.on_select)
      self.is_option_selected = True
      done()

    selected_item = self.tree.selection()[0]

    option1, option2 = self.tree.item(selected_item, 'values')

    self.dialog = ctk.CTkToplevel(self)

    self.dialog.title("Edit Option 2")

    first_opt = ctk.CTkLabel(self.dialog, text=f"{option1}")

    first_opt.grid(row=0, column=0, pady=20)

    self.box_option2_edit_val = ctk.StringVar()
    self.box_option2_edit = ctk.CTkComboBox(self.dialog,
                                            values=self.second_options,
                                            variable=self.box_option2_edit_val)
    self.box_option2_edit.set(option2)
    self.box_option2_edit.grid(row=0, column=1, pady=20)
    self.confirm_edit = ctk.CTkButton(self.dialog,
                                      text="Done",
                                      command=confirm_or_cancel)
    self.confirm_edit.grid(row=1, column=0)

  def delete_option(self):
    selected_item = self.tree.selection()[0]
    option1 = self.tree.item(selected_item, 'values')[0]
    self.tree.delete(selected_item)
    self.options.append(option1)
    self.options.sort()
    self.box_option_scroll.configure(values=self.options)
    self.selections.pop(option1)
    self.is_option_selected = False
    self.close_dialog()

  def on_select(self, event):
    if self.is_option_selected:
      self.is_option_selected = False
      return
    self.add_btn.configure(state="disabled")

    self.edit = ctk.CTkButton(self.display_box,
                              text="Edit",
                              command=self.edit_option)
    self.edit.grid(row=1, column=0)

    self.delete = ctk.CTkButton(self.display_box,
                                text="Delete",
                                command=self.delete_option)
    self.delete.grid(row=1, column=1)

    self.is_option_selected = True

  def get_selection(self):
    return self.selections


class Damage_Selection(ctk.CTkFrame):

  def __init__(self, *args, header_name="Vinyl Damages", **kwargs):
    super().__init__(*args, **kwargs)
    self.header_label = ctk.CTkLabel(self, text=header_name, font=("Helvetica", 18))
    self.header_label.grid(row=0, column=0, columnspan=6, sticky='ew')
    self.options = [
        "traces", "handling traces", "hairline", "hairlines", "sleeve dust",
        "sleeve rubs", "scuffings", "scuffs", "markings", "marks",
        "blemishing", "blemishes", "prints", "spindle marks", "ring wear",
        "corner wear"
    ]
    self.second_options = [
        "subtle", "faint", "barely-visible", "light", "minor", "occassional",
        "stray", "scattered", "mild", "moderate", "typical", "pronounced",
        "considerable", "severe"
    ]

    self.selections = {}
    self.is_option_selected = False
    self.main_func()

  def main_func(self):

    self.box_var = StringVar()
    self.box_option = ctk.CTkComboBox(self,
                                      variable=self.box_var,
                                      state="readonly")
    self.box_option_scroll = CTkScrollableDropdown.CTkScrollableDropdown(
        attach=self.box_option, values=self.options)
    self.box_option.grid(row=1,
                         column=0,
                         columnspan=2,
                         sticky='w',
                         pady=(10, 20),
                         padx=10)

    self.box_var2 = StringVar()
    self.box_option2 = ctk.CTkComboBox(self,
                                       variable=self.box_var2,
                                       state="readonly")
    self.box_option2_scroll = CTkScrollableDropdown.CTkScrollableDropdown(
        attach=self.box_option2, values=self.second_options)
    self.box_option2.grid(row=1,
                          column=2,
                          columnspan=2,
                          sticky='w',
                          pady=(10, 20),
                          padx=10)

    self.display_box = ctk.CTkFrame(self, height=100, width=300)
    self.display_box.grid(row=1,
                          column=4,
                          rowspan=4,
                          sticky='w',
                          pady=(10, 20),
                          padx=10)

    self.tree = ttk.Treeview(self.display_box,
                             columns=('Damage', 'Severity'),
                             show='headings',
                             height=8)
    self.tree.heading('Damage', text='Damage')
    self.tree.heading('Severity', text='Severity')

    self.add_btn = ctk.CTkButton(self, text="Add", command=self.box_selected)
    self.add_btn.grid(row=3, column=0, columnspan=2, sticky='e', padx=10)

    self.tree.grid(row=0,
                   column=0,
                   columnspan=2,
                   sticky='w',
                   pady=(10, 20),
                   padx=10)

    self.tree.bind('<<TreeviewSelect>>', self.on_select)

  def box_selected(self):
    self.selections[self.box_var.get()] = self.box_var2.get()
    self.tree.insert('',
                     'end',
                     values=(self.box_var.get(), self.box_var2.get()))
    idx = self.options.index(self.box_var.get())
    self.options.pop(idx)
    self.box_option_scroll.configure(values=self.options)
    self.box_var.set("")
    self.box_var2.set("")

  def close_dialog_and_reset(self):
    self.edit.destroy()
    self.delete.destroy()
    self.add_btn.configure(state="normal")
    self.edit = None
    self.delete = None
    self.is_option_selected = True

  def close_dialog(self):
    self.close_dialog_and_reset()

  def edit_option(self):

    def done():
      self.confirm_edit.destroy()
      self.confirm_edit = None
      self.dialog.destroy()
      self.is_option_selected = True
      self.close_dialog()

    def confirm_or_cancel():
      self.selections[option1] = self.box_option2_edit_val.get()
      tree_item = self.tree.selection()[0]
      self.tree.delete(tree_item)
      self.tree.unbind('<<TreeviewSelect>>')
      self.tree.insert('',
                       'end',
                       values=(option1, self.box_option2_edit_val.get()))
      self.tree.bind('<<TreeviewSelect>>', self.on_select)
      self.is_option_selected = True
      done()

    selected_item = self.tree.selection()[0]

    option1, option2 = self.tree.item(selected_item, 'values')

    self.dialog = ctk.CTkToplevel(self)

    self.dialog.title("Edit Option 2")

    first_opt = ctk.CTkLabel(self.dialog, text=f"{option1}")

    first_opt.grid(row=0, column=0, pady=20)

    self.box_option2_edit_val = ctk.StringVar()
    self.box_option2_edit = ctk.CTkComboBox(self.dialog,
                                            values=self.second_options,
                                            variable=self.box_option2_edit_val)
    self.box_option2_edit.set(option2)
    self.box_option2_edit.grid(row=0, column=1, pady=20)
    self.confirm_edit = ctk.CTkButton(self.dialog,
                                      text="Done",
                                      command=confirm_or_cancel)
    self.confirm_edit.grid(row=1, column=0)

  def delete_option(self):
    selected_item = self.tree.selection()[0]
    option1 = self.tree.item(selected_item, 'values')[0]
    self.tree.delete(selected_item)
    self.options.append(option1)
    self.options.sort()
    self.box_option_scroll.configure(values=self.options)
    self.selections.pop(option1)
    self.is_option_selected = False
    self.close_dialog()

  def on_select(self, event):
    if self.is_option_selected:
      self.is_option_selected = False
      return
    self.add_btn.configure(state="disabled")

    self.edit = ctk.CTkButton(self.display_box,
                              text="Edit",
                              command=self.edit_option)
    self.edit.grid(row=1, column=0)

    self.delete = ctk.CTkButton(self.display_box,
                                text="Delete",
                                command=self.delete_option)
    self.delete.grid(row=1, column=1)

    self.is_option_selected = True

  def get_selection(self):
    return self.selections


class DescriptionInputFrame(ctk.CTkFrame):

  def __init__(self, master, *args, **kwargs):
    super().__init__(master, *args, **kwargs)
    self.desc_data = {}

    def save():
      self.desc_data['artist'] = artist_text.get()
      self.desc_data['title'] = title_text.get()
      self.desc_data['type'] = types.get()
      self.desc_data["Condition"] = self.condition_frame.get_condition()
      self.master.save_data(self.desc_data)

    self.artist_title = ctk.CTkFrame(self)
    self.artist_title.grid(row=0,
                           column=0,
                           columnspan=2,
                           rowspan=3,
                           sticky='nsew',
                           pady=10,)

    # ---> ARTIST INPUT <--- #
    artist_label = ctk.CTkLabel(self.artist_title, text="Artist:", font=("Helvetica", 18))
    #artist_label.grid(row=1, column=2, padx=5, pady=10)
    artist_label.grid(row=0, column=0)

    artist_text = ctk.CTkEntry(self.artist_title, height=1, width=250)
    artist_text.grid(row=0, column=1, padx=20, pady=20, columnspan=2)

    # ---> TITLE INPUT <--- #
    title_label = ctk.CTkLabel(self.artist_title, text="Title:", font=("Helvetica", 18))
    #title_label.grid(row=2, column=2, padx=5, pady=10)
    title_label.grid(row=1, column=0)

    title_text = ctk.CTkEntry(self.artist_title, height=1, width=250)
    title_text.grid(row=1, column=1, padx=20, pady=20, columnspan=2)

    # ---> TYPE RADIO BUTTONS <--- #

    self.type_frame = ctk.CTkFrame(self)
    self.type_frame.grid(row=0,
                         column=2,
                         columnspan=4,
                         rowspan=3,
                         sticky='nsew',
                         pady=10)
    type_label = ctk.CTkLabel(self.type_frame, text="Type:", font=("Helvetica", 18))
    type_label.grid(row=2, column=0, padx=40)

    types_list = [
        "LP", "12\"", "ABC2", "2xLP", "EP", "ABC3", "3xLP", "ABC1", "BOX"
    ]
    types = ctk.StringVar(self.type_frame, "Type")

    r, c = 0, 0
    for i, type in enumerate(types_list):
      if i % 3 == 0:
        r += 1
        c = 0
      type_opt = ctk.CTkRadioButton(self.type_frame,
                                    text=type,
                                    variable=types,
                                    value=type)

      type_opt.grid(row=r, column=c + 1, padx=10, pady=10)

      c += 1

    # ---> DIVIDER <--- #
    divider = ctk.CTkFrame(self, height=2, fg_color="gray")
    divider.grid(row=4, column=0, columnspan=17, sticky='we', padx=5, pady=5)

    # ---> DIVIDER <--- #
    divider = ctk.CTkFrame(self, height=2, fg_color="gray")
    divider.grid(row=8, column=0, columnspan=17, sticky='we', padx=5, pady=5)

    self.condition_frame = Condition(self)
    self.condition_frame.grid(row=9,
                              column=0,
                              columnspan=17,
                              sticky='we',
                              padx=5,
                              pady=5)

    save_button = ctk.CTkButton(self, text="Next", command=save)
    save_button.grid(row=15, column=2, columnspan=1, padx=20, pady=20)

  def get_desc_data(self):
    return self.desc_data

class AI_Frame(ctk.CTkFrame):
  def  __init__(self, master=None, condition=None, vinyl_dmg=None, jacket_dmg=None, **kwargs):
    super().__init__(master, **kwargs)
    self.configure( width=900, height=600)
    self._condition = condition
    self._vinyl_dmg = vinyl_dmg
    self._jacket_dmg = jacket_dmg

  def desc(self):

    ai_label = ctk.CTkLabel(self, text="Artificial Intelligence (AI)", font=("Helvetica", 18))
    ai_label.grid(row=0, column=0,  columnspan=5, sticky='ew')

    '''condition = Condition.get_condition()

    jacket_dmg = Damage_Selection_Jacket.get_selection()
    vinyl_dmg = Damage_Selection.get_selection()'''

    # ---> FILE HANDLING <--- #
    xl_file = xl.open_excel_file('WebLP Master NEW.xlsx')

    df = xl_file.read_into_dataframe()

    filtered_df = df[df['Cond'] == self._condition]

    # -->--> Text Processing <--<-- #
    filtered_df['Description'] = filtered_df['Description'].str.lower()

    filtered_df['Description'] = filtered_df['Description'].astype(str).apply(
        word_tokenize)

    stop_words = set(stopwords.words('english'))

    filtered_df['Description'] = filtered_df['Description'].apply(
        lambda x: [word for word in x if word not in stop_words])

    # ---> COUNTER <--- #
    word_counts = Counter()
    for notes in filtered_df['Description']:
      word_counts.update(notes)

    # -->--> Identify Common Words <--<-- #
    # ->->-> Change number for the amount of words <-<-<- #
    most_common_words = word_counts.most_common(20)

    # ---> TF-IDF <--- #
    filtered_df['Description'] = filtered_df['Description'].apply(' '.join)

    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(filtered_df['Description'])
    feature_names = tfidf_vectorizer.get_feature_names_out()

    mean_tfidf_scores = tfidf_matrix.mean(axis=0)

    mean_tfidf_scores = mean_tfidf_scores.tolist()[0]

    word_tfidf_scores = dict(zip(feature_names, mean_tfidf_scores))

    self.top_words_tfidf = [(feature_names[i], mean_tfidf_scores[i])
                            for i in range(len(mean_tfidf_scores))]

    # ---> CHAT-3 AI <--- #
    # -->--> Set up GPT API key <--<-- #
    '''OPENAI_API_KEY = 

    client = OpenAI(api_key=OPENAI_API_KEY,
                    organization='org-kcRkG3XdvJvZ7n96rmg9do6k')
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    response_api = requests.get("http://api.openai.com/v1/chat/completions",
                                headers=headers)'''

    # -->--> Prompt usng the common words/phrases <--<-- #
    prompt = "PLEASE LEAVE DESCRIPTION IN 2 SENTENCES: Based on the commonly used words and phrases in the dataset for the condition '" + self._condition + "', please generate a general description for the corresponding vinyl: " + "".join(
        [word for word, _ in self.top_words_tfidf]
    ) + "\nMake sure the first sentence is about the vinyl and the second sentence is about the jacket. Also, use these python dictionary to write an accurate decription on the vinyl damage: " + str(self._vinyl_dmg) + " and jacket damage: " + str(self._jacket_dmg) + " ONLY IF THE DAMAGE IS PRESENT. If the damage is not present, please do not include the vinyl or jacket damage in the description. Thank you."

    # --> UNCOMMENT WHEN READY TO USE API <-- #
    '''messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    }, {
        "role": "user",
        "content": prompt
    }]

    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=messages)
    generated_description = response.choices[0].message.content.strip()'''

    
    self.AIDescriptionDiag = ctk.CTkFrame(self, height=600, width=900)
    self.AIDescriptionDiag.grid(row=1, column=0, columnspan=5, sticky='nsew')

    self.AIDescription_label = ctk.CTkLabel(self.AIDescriptionDiag,
                                            text="AI Description", font=("Helvetica", 18))
    self.AIDescription_label.grid(row=0, column=0, columnspan=5, pady=20, sticky='nsew')

    self.AIDescription_text = ctk.CTkTextbox(self.AIDescriptionDiag,
                                           height=300,
                                           width=300, wrap="word")
    self.AIDescription_text.configure(state="normal")
    self.AIDescription_text.delete("0.0", tk.END)
    
    #-- CHANGE TO generated_description WHEN API IS READY --#
    self.AIDescription_text.insert("0.0", prompt)
    self.AIDescription_text.grid(row=1, column=1, columnspan=3, pady=20, padx=20, sticky='nsew')

    self.AIDescription_button = ctk.CTkButton(self.AIDescriptionDiag,
                                              text="Back",
                                              command=self.master.prev_frame)
    self.AIDescription_button.grid(row=2, column=1, pady=50, padx=50)

    self.AIDescription_button = ctk.CTkButton(self.AIDescriptionDiag,
                                              text="Save",
                                              command=NONE)
    self.AIDescription_button.grid(row=2, column=2, pady=20, padx=50)
  
  @property
  def condition(self):
    return self._condition
  
  @property
  def vinyl_dmg(self):
    return self._vinyl_dmg
  
  @property
  def jacket_dmg(self):
    return self._jacket_dmg

  @condition.setter
  def condition(self, cnd):
    self._condition = cnd

  @vinyl_dmg.setter
  def vinyl_dmg(self, vnyl):
    self._vinyl_dmg = vnyl

  @jacket_dmg.setter
  def jacket_dmg(self, jckt):
    self._jacket_dmg = jckt


class AIApp(ctk.CTkFrame):

  def __init__(self, master=None, **kwargs):
    super().__init__(master, **kwargs)
    # ---> Create double linked list for frame navigation <--- #
    self.current = None
    self.vinyl_data = {}
    self.description_frame = DescriptionInputFrame(self)
    self.damage_frame = self.build_second_frame()
    self.ai_frame = AI_Frame(self)
    threading.Thread(target=self.nltk_packages, daemon=True).start()
    self.frames_ll = self.LL_Frames([self.description_frame, self.damage_frame, self.ai_frame])
    self.set_current(self.frames_ll.head)
    self.begin()

  def nltk_packages(self):
    nltk.download('punkt')
    nltk.download('stopwords')

  def begin(self):
    self.current.data.grid(row=0, column=0, sticky='nsew')

  def save_data(self, vinyl_data):
    self.vinyl_data.update(vinyl_data)
    self.next_frame()

  def next_frame(self):
    self.current.data.grid_forget()
    self.set_current(self.current.next)
    if self.current.data == self.ai_frame:
      self.ai_frame.grid(row=0, column=0, sticky='nsew')
      self.ai_frame.condition = self.vinyl_data["Condition"]
      self.ai_frame.vinyl_dmg = self.vinyl_data["Vinyl Damage"]
      self.ai_frame.jacket_dmg = self.vinyl_data["Jacket Damage"]
      self.ai_frame.desc()
    else:
      self.current.data.grid(row=0, column=0, sticky='nsew')

  def build_second_frame(self):
    self.secondframe = ctk.CTkScrollableFrame(self,
                                              height=700,
                                              width=900,
                                              orientation='vertical')

    self.secondsection = Damage_Selection(self.secondframe)
    self.secondsection.grid(row=0, column=0, sticky='nsew')

    self.thirdsection = Damage_Selection_Jacket(self.secondframe)
    self.thirdsection.grid(row=1, column=0, sticky='nsew')

    self.btns = ctk.CTkFrame(self.secondframe)
    self.btns.grid(row=2, column=0, columnspan=3, pady= 10)

    back_button = ctk.CTkButton(self.btns,
                                text="Back",
                                command=self.prev_frame)
    back_button.grid(row=0, column=0, columnspan=2, sticky='w', padx=10)

    next_button = ctk.CTkButton(self.btns,
                                text="Next",
                                command=lambda: self.save_data({"Vinyl Damage": self.secondsection.get_selection(), "Jacket Damage": self.thirdsection.get_selection()}))
    next_button.grid(row=0, column=2, columnspan=2, sticky='e', padx=10)

    return self.secondframe

  def prev_frame(self):
    self.current.data.grid_forget()
    self.set_current(self.current.prev)
    self.current.data.grid(row=0, column=0, sticky='nsew')

  def LL_Frames(self, frames):
    # --> Double Linked List of Frames <-- #
    return dll.DoublyLinkedList(frames)
  
  def set_current(self, current):
    self.current = current
