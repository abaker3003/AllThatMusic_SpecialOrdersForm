import torch
import torch.nn as nn
import torch.optim as optim
import xlfile as xl
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from openai import OpenAI
import requests
import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import tkinter.messagebox as msgbox
from matplotlib import artist
import os

class Damage_Selection(ctk.CTkFrame):
    def __init__(self, *args, header_name="Add Damages", **kwargs):
        super().__init__(*args, **kwargs)
        self.options = ["A", "B", "C", "D", "E"]
        self.second_options = ["1", "2", "3", "4", "5"]

        self.selections = {}
        self.is_option_selected = False
        self.main_func()

    def main_func(self):
        
        self.box_var = ctk.StringVar()
        self.box_option = ctk.CTkComboBox(self, values=self.options, variable=self.box_var)
        self.box_option.grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 20), padx=10)
        self.box_var2 = ctk.StringVar()
        box_option2 = ctk.CTkComboBox(self, values=self.second_options, variable=self.box_var2)
        box_option2.grid(row=0, column=2, columnspan=2, sticky='w', pady=(10, 20), padx=10)


        self.display_box = ctk.CTkFrame(self, height=500, width=300)
        self.display_box.grid(row=0, column=4, sticky='w', pady=(10, 20), padx=10)

        #self.selected_options = ctk.CTkTextbox(self.display_box, height=400, width=250, state="disabled")
        self.tree = ttk.Treeview(self.display_box, columns=('Option 1', 'Option 2'), show='headings')
        self.tree.heading('Option 1', text='Option 1')
        self.tree.heading('Option 2', text='Option 2')


        self.add_btn = ctk.CTkButton(self, text="Add", command=self.box_selected)
        self.add_btn.grid(row=1, column=0, columnspan=2, sticky='w')

        #self.selected_options.grid(row=0, column=0, sticky='w', pady=(10, 20), padx=10)

        self.tree.grid(row=0, column=0, columnspan=2, sticky='w', pady=(10, 20), padx=10)

        #self.selected_options.bind("<Button-1>", lambda e: self.tree.focus_set(self.tree.nearest(e.y)))

        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def box_selected(self):
        self.selections[self.box_var.get()] = self.box_var2.get()
        self.tree.insert('', 'end', values=(self.box_var.get(), self.box_var2.get()))
        idx = self.options.index(self.box_var.get())
        self.options.pop(idx)
        print(idx)
        self.box_option.configure(values=self.options) 
        self.box_var.set("")
        self.box_var2.set("")

    def close_dialog_and_reset(self):
        print("close_dialog_and_reset()")
        self.edit.destroy()
        self.delete.destroy()
        print("Delete Button and Edit Button Destroyed")
        self.add_btn.configure(state="normal")
        print("Add Button Re-enabled")
        self.edit = None
        self.delete = None
        print("Edit button and Delete button are None")
        self.is_option_selected = True

    def close_dialog(self):
        print("close_dialog()")
        self.close_dialog_and_reset()

    def edit_option(self):

        def done():
            print("done()")
            self.confirm_edit.destroy()
            self.confirm_edit = None
            self.dialog.destroy()
            print("Edit Dialog Destroyed")
            self.is_option_selected = True
            self.close_dialog()
            

        def confirm_or_cancel():
            self.selections[option1] = self.box_option2_edit_val.get()
            tree_item = self.tree.selection()[0]
            self.tree.delete(tree_item)
            self.tree.unbind('<<TreeviewSelect>>')
            self.tree.insert('', 'end', values=(option1, self.box_option2_edit_val.get()))
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
        self.box_option2_edit = ctk.CTkComboBox(self.dialog, values=self.second_options, variable=self.box_option2_edit_val)
        self.box_option2_edit.set(option2)
        self.box_option2_edit.grid(row=0, column=1, pady=20)
        self.confirm_edit = ctk.CTkButton(self.dialog, text="Done", command=confirm_or_cancel)
        self.confirm_edit.grid(row=1, column=0)

    def delete_option(self):
        selected_item = self.tree.selection()[0]
        option1 = self.tree.item(selected_item, 'values')[0]
        self.tree.delete(selected_item)
        self.options.append(option1)
        self.options.sort()
        self.box_option.configure(values=self.options)
        self.selections.pop(option1)
        self.is_option_selected = False
        self.close_dialog()

    def on_select(self, event):
        if self.is_option_selected:
            self.is_option_selected = False
            return
        print("Add Button Disabled")
        self.add_btn.configure(state="disabled")

        print("Edit and Delete buttons created")

        self.edit = ctk.CTkButton(self.display_box, text="Edit", command=self.edit_option)
        self.edit.grid(row=1, column=0, pady=20)

        self.delete = ctk.CTkButton(self.display_box, text="Delete", command=self.delete_option)
        self.delete.grid(row=1, column=1, pady=20)

        self.is_option_selected = True



class Base(ctk.CTkFrame):
    def __init__(self, *args, header_name="Prep crate with AI", **kwargs):
        super().__init__(*args, **kwargs)
        self.grid()

class DescriptionInputFrame(Base):
    def __init__(self, *args, header_name="Prep crate with AI", **kwargs):
        super().__init__(*args, **kwargs)

        def save():
            self.selected_condition = conditions.get()
            self.selected_damages = {self.dmg_texts[i]: self.severity_vars[i].get() for i, dmg in enumerate(self.dmgs) if dmg.get()}
            save_button['state'] = "DISABLED"
            self.AIDescriptionFrame()

        # ---> ARTIST INPUT <--- #
        artist_label = ctk.CTkLabel(self, text="Artist:")
        #artist_label.grid(row=1, column=2, padx=5, pady=10)
        artist_label.grid(row=1, column=2)

        artist_text = ctk.CTkEntry(self, height=1, width=30)
        artist_text.grid(row=1, column=3, padx=20, pady=20, columnspan=3)

        # ---> TITLE INPUT <--- #
        title_label = ctk.CTkLabel(self, text="Title:")
        #title_label.grid(row=2, column=2, padx=5, pady=10)
        title_label.grid(row=2, column=2)

        title_text = ctk.CTkEntry(self, height=1, width=30)
        title_text.grid(row=2, column=3, padx=20, pady=20, columnspan=3)

        # ---> TYPE RADIO BUTTONS <--- #
        type_label = ctk.CTkLabel(self, text="Type:")
        type_label.grid(row=2, column=7)

        types_list = ["LP", "12\"", "ABC2", "2xLP", "EP", "ABC3", "3xLP", "ABC1", "BOX"]
        types = ctk.StringVar(self, "Type")

        r, c = 0,0
        for i, type in enumerate(types_list):
            if i % 3 == 0:
                r += 1
                c = 0
            type_opt = ctk.CTkRadioButton(self, text=type, variable=types, value=type)
            type_opt.grid(row=r, column=c+8, padx=10)
            c += 1

        # ---> DIVIDER <--- #
        divider = ctk.CTkFrame(self, height=2, fg_color="gray")
        divider.grid(row=4, column=0, columnspan=17, sticky='we', padx=5, pady=5)

        # ---> DIVIDER <--- #
        divider = ctk.CTkFrame(self, height=2, fg_color="gray")
        divider.grid(row=8, column=0, columnspan=17, sticky='we', padx=5, pady=5)

        # ---> DESCRIPTION INPUT <--- #
        conditions_list = ["Good", "Very Good", "Fairly Good", "Fair", "New", "Poor"]
        conditions = ctk.StringVar(self, "Condition")

        for i, cond in enumerate(conditions_list):
            cond_opt = ctk.CTkRadioButton(self, text=cond, variable=conditions, value=cond)
            cond_opt.grid(row=9, column=i+4)

        damage_dict = {}
        damage_set_vinyl = ["traces", "handling traces", "hairline", "hairlines", "sleeve dust", "sleeve rubs", "scuffings", "scuffs", "markings", "marks", "blemishing", "blemishes", "prints", "spindle marks", "ring wear", "corner wear"]
        self.dmgs = []
        self.dmg_texts = []

        self.severity_frames = []
        self.severity_vars = []


        for i, dmg in enumerate(damage_set_vinyl):
            damages = ctk.IntVar()
            dmg_opt = ctk.CTkCheckBox(self, text=dmg, variable=damages)
            dmg_opt.grid(row=10, column=i, padx=10, pady=20)
            self.dmgs.append(damages)
            self.dmg_texts.append(dmg)


            severity_var = ctk.StringVar()
            self.severity_vars.append(severity_var)
            severity_frame = ctk.CTkFrame(self)
            severity_frame.grid(row=11, column=i, padx=5, pady=5)

            severity_list = ["subtle", "faint", "barely-visible", "light", "minor", "occassional", "stray", "scattered", "mild", "moderate", "typical", "pronounced", "considerable", "severe"]
            for j, severity in enumerate(severity_list):
                severity_opt = ctk.CTkRadioButton(severity_frame, text=severity, variable=severity_var, value=severity)
                severity_opt.grid(row=j, column=0, sticky="w")

            self.severity_frames.append(severity_frame)
            severity_frame.grid_remove()

            dmg_opt.configure(command=lambda i=i: self.radio_show_hide(i))

        save_button = ctk.CTkButton(self, text="Save", command=save)
        save_button.grid(row=15, column=7, columnspan=1, padx=20, pady=20)

    def radio_show_hide(self, i):
        if self.dmgs[i].get() == 1:
            self.severity_frames[i].grid()
        else:
            self.severity_frames[i].grid_remove()

    def AIDescription(self):

        nltk.download('punkt')
        nltk.download('stopwords')

        # ---> FILE HANDLING <--- #
        xl_file = xl.open_excel_file('WebLP Master NEW.xlsx')
        df = xl_file.read_into_dataframe()
        filtered_df = df[df['Cond'] == self.selected_condition]

        # -->--> Text Processing <--<-- #
        filtered_df['Description'] = filtered_df['Description'].str.lower()

        filtered_df['Description'] = filtered_df['Description'].astype(str).apply(word_tokenize)

        stop_words = set(stopwords.words('english'))

        filtered_df['Description'] = filtered_df['Description'].apply(lambda x: [word for word in x if word not in stop_words])


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

        # ---> CHAT-3 AI <--- #
        # -->--> Set up GPT API key <--<-- #
        OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

        client = OpenAI(
            api_key=OPENAI_API_KEY,
            organization='org-kcRkG3XdvJvZ7n96rmg9do6k'
        )
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        response_api = requests.get("http://api.openai.com/v1/chat/completions", headers=headers)

        # -->--> Prompt usng the common words/phrases <--<-- #
        prompt = "PLEASE LEAVE DESCRIPTION IN 2 SENTENCES: Based on the commonly used words and phrases in the dataset for the condition '" + self.selected_condition + "', please generate a general description for the corresponding vinyl: " + "".join([word for word, _ in self.top_words_tfidf]) + "\nMake sure the first sentence is about the vinyl and the second sentence is about the jacket. Also, use this python dictionary to write an accurate decription on the condition: " + str(self.selected_damages)
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]

        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages
        )
        generated_description = response.choices[0].message.content.strip()
        return generated_description

    def AIDescriptionFrame(self):
        ai_description = self.AIDescription()
        self.AIDescriptionDiag = ctk.CTkToplevel(self)
        self.AIDescriptionDiag.title("AI Description")
        self.AIDescriptionDiag.geometry("500x500")

        self.AIDescription_label = ctk.CTkLabel(self.AIDescriptionDiag, text="AI Description")
        self.AIDescription_label.grid(row=0, column=0, pady=20)

        self.AIDescription_text = ctk.CTkEntry(self.AIDescriptionDiag, height=10, width=50)
        self.AIDescription_text.configure(state="normal")
        self.AIDescription_text.insert("1.0", ai_description)
        self.AIDescription_text.grid(row=1, column=0, pady=20)

        self.AIDescription_button = ctk.CTkButton(self.AIDescriptionDiag, text="Generate", command=NONE)
        self.AIDescription_button.grid(row=2, column=0, pady=50, padx=50)

        self.AIDescription_button = ctk.CTkButton(self.AIDescriptionDiag, text="Save", command=NONE)
        self.AIDescription_button.grid(row=3, column=0, pady=20, padx=50)

'''
class AIApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI Chatbot")
        self.description_frame = DescriptionInputFrame(self)
        self.description_frame.grid()

if __name__ == "__main__":
    app = AIApp()
    app.mainloop()'''
