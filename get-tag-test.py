import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

input = sys.argv[1:]

root = tk.Tk()
label = tk.Label(root, text=input, font=("Comic Sans MS", 27))
label.pack(padx=20, pady=20)

root.mainloop()