import sys # allows input from cli
import tkinter as tk # provides GUI widgets
from tkinter import messagebox
import subprocess # allows for running commands in cmd
import urllib.parse # parses a given string to the proper URL format
import configparser # parses ini 
import random

# MPACS input
input = sys.argv[1:]

# Set global vars from MPACS input
# try:
#     mrn = input[0]
#     ipid = input[1]
#     pt_name = input[2]
#     accession = input[3]
# except IndexError as e:
#     print("Missing Patient Demographic")
#     print(f"Error: {e}")

#     root2 = tk.Tk()
#     root2.title("Deletion Request Error")
#     label = tk.Label(root2, text="Error: Missing Patient Demographics", font=("Arial", 16))
#     label.pack(padx=20, pady=20)

#     root2.mainloop()

#     quit()

# Hardcoded for testing
mrn = 'test' + str(random.randrange(999999999))
ipid = 'SOCAL_CSB'
pt_name = 'Python test'
accession = 'ACC' + str(random.randrange(999999999))
pt_demo_str = f"MRN: {mrn},\nIPID: {ipid}, \nPatient Name: {pt_name}, \nAccession #: {accession}"

class App:

    def __init__(self):

        # create root window
        self.root = tk.Tk()
        self.root.title("Image Deletion Request")
        self.root.geometry('600x520')
        self.root.eval('tk::PlaceWindow . center')

        # create widgets
        self.label = tk.Label(
            self.root, 
            text="Deletion request for\n the following exam:", 
            font=("Arial", 27))
        
        self.pt_demo_label = tk.Label(
            self.root, 
            text=pt_demo_str, 
            font=("Arial", 14),
            fg='#37afdb',justify='left')
        
        self.instruction = tk.Label(
            self.root, 
            text= "Please describe why these image(s) need to be deleted", 
            font=("Arial", 12))
        
        self.usr_justifctn = tk.Text(self.root, height=4)
        self.usr_justifctn.insert(1.0, "Deletion reason...")

        self.new_line = tk.Label(self.root, text= "\n", font=("Arial", 6))

        self.name_label = tk.Label(
            self.root, 
            text= "Please type your name here", 
            font=("Arial", 12))
        
        self.tech_name = tk.Text(self.root, height=1, width= 50)
        self.tech_name.insert(1.0, "Name...")

        self.submit_btn = tk.Button(
            self.root,
            text='Submit',
            command = self.submit)
        
        # bind text boxes to delete on first click 
        self.usr_justifctn.bind("<Button-1>", self.on_click)
        self.tech_name.bind("<Button-1>", self.on_click)

        # pack widgets to root window
        self.label.pack(padx=20, pady=20)
        self.pt_demo_label.pack(padx=20, pady=20)
        self.instruction.pack()
        self.usr_justifctn.pack(padx=50)
        self.new_line.pack()
        self.name_label.pack()
        self.tech_name.pack(pady=10)
        self.submit_btn.pack(pady=20)

        self.root.mainloop()
        

    # class functions
    def submit(self):

        # Parse INI
        config = configparser.ConfigParser()
        config.read('config.ini')
        url = config.get('URLs', 'FORMURL')

        # Get user input and inject into URL
        user_msg = self.usr_justifctn.get('1.0', tk.END)
        tech = self.tech_name.get('1.0', tk.END)
        params = {
            'entry.501677638': ipid, 
            'entry.349499540': pt_name, 
            'entry.800935706': mrn, 
            'entry.2083454847' : accession, 
            'entry.1340586078' : user_msg, 
            'entry.1963475195' : tech
            }

        # Replace 'chrome' with 'google-chrome' on Linux
        chrome_command = "start chrome " + '"' + url + urllib.parse.urlencode(params) + '"'
        
        subprocess.run(chrome_command, shell=True)
        messagebox.showinfo("Payload deployed!", "Thank you for your request!")
        self.root.destroy()


    def on_click(self, event):
        event.widget.delete('1.0', tk.END) # clears string




App()
"""
PURPOSE:
orchestrate sending relevant DICOM info to google form
1. take DICOM values from PACS
2. take deletion justification and tech name from GUI

TODO:
set macro to run this script
1.
get user input(DICOM tag) from cli
print that input
test this from cli

display output in GUI window

CONFIRMED:
can turn py into exe
exe can still take cli args
PyInstaller or cx_Freeze for turing py into exe

REF:
https://www.tcl.tk/man/tcl8.6/TkCmd/entry.html

"""
