import tkinter as tk
import tkinter
from tkinter.constants import END, INSERT
from tkinter.ttk import *
from tkinter import scrolledtext
from ttkthemes import ThemedTk


window = ThemedTk(theme='arc')
window.title("First Window")
window.geometry("350x200")


txt = scrolledtext.ScrolledText(window, width=40, height=10)
txt.grid(column=0, row=0)

txt.delete(1,END);

window.mainloop()
