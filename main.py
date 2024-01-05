import tkinter as tk
import subprocess
import datetime
import generators as gn
import xlfile as xl


window = tk.Tk()
window.title("Special Order")

ticket_num = gn.ticketnum()
label = tk.Label(window, text=ticket_num)
label.pack()

x = xl.openxl()

window.mainloop()