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
import tkinter.messagebox as msgbox
from matplotlib import artist
import os

class Base(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()

class DescriptionInputFrame(Base):
    def __init__(self, master=None):
        super().__init__(master)

        def save():
            self.selected_condition = conditions.get()
            self.selected_damages = {self.dmg_texts[i]: self.severity_vars[i].get() for i, dmg in enumerate(self.dmgs) if dmg.get()}
            save_button['state'] = DISABLED
            self.AIDescriptionFrame()

        # ---> ARTIST INPUT <--- #
        artist_label = tk.Label(self, text="Artist:")
        #artist_label.grid(row=1, column=2, padx=5, pady=10)
        artist_label.grid(row=1, column=2)

        artist_text = tk.Text(self, height=1, width=30)
        artist_text.grid(row=1, column=3, padx=20, pady=20, columnspan=3)

        # ---> TITLE INPUT <--- #
        title_label = tk.Label(self, text="Title:")
        #title_label.grid(row=2, column=2, padx=5, pady=10)
        title_label.grid(row=2, column=2)

        title_text = tk.Text(self, height=1, width=30)
        title_text.grid(row=2, column=3, padx=20, pady=20, columnspan=3)

        # ---> TYPE RADIO BUTTONS <--- #
        type_label = tk.Label(self, text="Type:")
        type_label.grid(row=2, column=7)

        types_list = ["LP", "12\"", "ABC2", "2xLP", "EP", "ABC3", "3xLP", "ABC1", "BOX"]
        types = StringVar(self, "Type")

        r, c = 0,0
        for i, type in enumerate(types_list):
            if i % 3 == 0:
                r += 1
                c = 0
            type_opt = Radiobutton(self, text=type, variable=types, value=type)
            type_opt.grid(row=r, column=c+8, padx=10)
            c += 1

        # ---> DIVIDER <--- #
        divider = tk.Frame(self, height=2, bd=1, relief="sunken")
        divider.grid(row=4, column=0, columnspan=17, sticky='we', padx=5, pady=5)

        # ---> DIVIDER <--- #
        divider = tk.Frame(self, height=2, bd=1, relief="sunken")
        divider.grid(row=8, column=0, columnspan=17, sticky='we', padx=5, pady=5)

        # ---> DESCRIPTION INPUT <--- #
        conditions_list = ["Good", "Very Good", "Fairly Good", "Fair", "New", "Poor"]
        conditions = StringVar(self, "Condition")

        for i, cond in enumerate(conditions_list):
            cond_opt = Radiobutton(self, text=cond, variable=conditions, value=cond)
            cond_opt.grid(row=9, column=i+4)

        damage_dict = {}
        damage_set_vinyl = ["traces", "handling traces", "hairline", "hairlines", "sleeve dust", "sleeve rubs", "scuffings", "scuffs", "markings", "marks", "blemishing", "blemishes", "prints", "spindle marks", "ring wear", "corner wear"]
        self.dmgs = []
        self.dmg_texts = []

        self.severity_frames = []
        self.severity_vars = []


        for i, dmg in enumerate(damage_set_vinyl):
            damages = tk.IntVar()
            dmg_opt = tk.Checkbutton(self, text=dmg, variable=damages)
            dmg_opt.grid(row=10, column=i, padx=10, pady=20)
            self.dmgs.append(damages)
            self.dmg_texts.append(dmg)


            severity_var = tk.StringVar()
            self.severity_vars.append(severity_var)
            severity_frame = tk.Frame(self)
            severity_frame.grid(row=11, column=i, padx=5, pady=5)

            severity_list = ["subtle", "faint", "barely-visible", "light", "minor", "occassional", "stray", "scattered", "mild", "moderate", "typical", "pronounced", "considerable", "severe"]
            for j, severity in enumerate(severity_list):
                severity_opt = tk.Radiobutton(severity_frame, text=severity, variable=severity_var, value=severity)
                severity_opt.grid(row=j, column=0, sticky="w")

            self.severity_frames.append(severity_frame)
            severity_frame.grid_remove()

            dmg_opt.config(command=lambda i=i: self.radio_show_hide(i))

        save_button = ttk.Button(self, text="Save", command=save)
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
        self.AIDescriptionDiag = tk.Toplevel(self.master)
        self.AIDescriptionDiag.title("AI Description")
        self.AIDescriptionDiag.geometry("500x500")

        self.AIDescription_label = tk.Label(self.AIDescriptionDiag, text="AI Description")
        self.AIDescription_label.grid(row=0, column=0, pady=20)

        self.AIDescription_text = tk.Text(self.AIDescriptionDiag, height=10, width=50)
        self.AIDescription_text.config(state="normal")
        self.AIDescription_text.insert("1.0", ai_description)
        self.AIDescription_text.grid(row=1, column=0, pady=20)

        self.AIDescription_button = ttk.Button(self.AIDescriptionDiag, text="Generate", command=NONE)
        self.AIDescription_button.grid(row=2, column=0, pady=50, padx=50)

        self.AIDescription_button = ttk.Button(self.AIDescriptionDiag, text="Save", command=NONE)
        self.AIDescription_button.grid(row=3, column=0, pady=20, padx=50)


class AIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Chatbot")
        self.description_frame = DescriptionInputFrame(self)
        self.description_frame.grid()

if __name__ == "__main__":
    app = AIApp()
    app.mainloop()
