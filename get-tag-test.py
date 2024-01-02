# import sys
# import tkinter as tk
# from tkinter import ttk
# from tkinter import messagebox

# input = sys.argv[1:]

# root = tk.Tk()
# label = tk.Label(root, text=input, font=("Comic Sans MS", 27))
# label.pack(padx=20, pady=20)

# root.mainloop()

import configparser

# Create a ConfigParser object
config = configparser.ConfigParser()

# Read the INI file
config.read('config.ini')

# Access the variable from the specified section
variable_value = config.get('URLs', 'FORMURL')

# Now you can use the variable in your script
print("variable_name:", variable_value)