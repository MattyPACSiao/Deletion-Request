import sys # allows input from cli
import tkinter as tk # provides GUI widgets
from tkinter import messagebox
import subprocess # allows for running commands in cmd
import urllib.parse # parses a given string to the proper URL format
import configparser # parses ini 
import random
import webbrowser
import os
import ctypes

# Get the current working directory to use in "required files" check
_cwd = os.path.realpath(__file__)
_cwd = _cwd.replace(__file__,"")

# Let's make sure we got the files we need for program to function.
if os.path.exists(_cwd+"icon.ico") and os.path.exists(_cwd+"GitHub_Logo_small.png") and os.path.exists(_cwd+"config.ini"):
    print ("icon.ico: "+ str(os.path.exists(_cwd+"icon.ico")))
    print ("GitHub Logo: "+ str(os.path.exists(_cwd+"GitHub_Logo_small.png")))
    print ("config.ini: "+ str(os.path.exists(_cwd+"config.ini")))
    print("Required files present")
else:
    print('Required files missing')
    print ("icon.ico: "+ str(os.path.exists(_cwd+"icon.ico")))
    print ("GitHub Logo: "+ str(os.path.exists(_cwd+"GitHub_Logo_small.png")))
    print ("config.ini: "+ str(os.path.exists(_cwd+"config.ini")))
    root1 = tk.Tk()
    root1.title('Required Files Missing')
    label = tk.Label(root1, text=f'Files required for proper program execution missing.\n\n' + "icon.ico: "+ str(os.path.exists(_cwd+"icon.ico")) + "\n" + "GitHub Logo: "+ str(os.path.exists(_cwd+"GitHub_Logo_small.png")) + "\n" + "config.ini: "+ str(os.path.exists(_cwd+"config.ini")) + "\n\nProgram will close.", font=('Arial', 16))
    label.pack(padx=20, pady=20)

    root1.mainloop()

    quit()

# MPACS input
DICOM_tags = sys.argv[1:]
tags_to_string = ''.join(DICOM_tags)

# Passing "/TEST" (case sensitive) to the program will launch a version that doesn't require MPACS input.
if tags_to_string.find("/TEST"):
    # handle whitespaces in demographics
    input = tags_to_string.split('?')

    # Set global vars from MPACS input
    try:
        mrn = input[0]
        ipid = input[1]
        pt_name = input[2]
        accession = input[3]
    except IndexError as e:
        print('Missing Patient Demographic')
        print(f'Error: {e}')

        root2 = tk.Tk()
        root2.title('Deletion Request Error')
        label = tk.Label(root2, text=f'Missing Patient Demographics\nError:{e}\nReceived input of: {input}\n\nPlease make sure that your exam is not missing any of the following info: MRN, Patient name, Accession#', font=('Arial', 16))
        label.pack(padx=20, pady=20)

        root2.mainloop()

        quit()
else:
    # Hardcoded for testing
    mrn = 'test' + str(random.randrange(999999999))
    ipid = 'SOCAL_CSB'
    pt_name = 'Python test'
    accession = 'ACC' + str(random.randrange(999999999))

# Function to retrieve the "Display Name" of the currently logged in user.
def get_display_name():
        GetUserNameEx = ctypes.windll.secur32.GetUserNameExW
        NameDisplay = 3
     
        size = ctypes.pointer(ctypes.c_ulong(0))
        GetUserNameEx(NameDisplay, None, size)
     
        nameBuffer = ctypes.create_unicode_buffer(size.contents.value)
        GetUserNameEx(NameDisplay, nameBuffer, size)
        return nameBuffer.value

pt_demo_str = f'MRN: {mrn},\nIPID: {ipid}, \nPatient Name: {pt_name}, \nAccession #: {accession}'

class App:

    # If both "reason for deletion" and "user requesting deletion" contain text, enable the submit button (disabled by default)
    def configure_submit_button(self,event):
        if self.usr_justifctn_box.get("1.0",'end-1c') and self.name_txt_box.get("1.0",'end-1c'):
            self.submit_btn.config(state = tk.NORMAL)
        else:
            self.submit_btn.config(state = tk.DISABLED)

    def __init__(self):

        # create root window
        self.root = tk.Tk()
        self.root.iconbitmap(default='icon.ico')
        self.root.title('Image Deletion Request')
        self.root.geometry('600x650')
        # self.root.eval('tk::PlaceWindow . center')

        # create widgets
        self.debug = tk.Label(
            self.root, 
            text=input, 
            font=('Arial', 27))

        self.label = tk.Label(
            self.root, 
            text='Image deletion request for\n the following exam:', 
            font=('Arial', 27))
        
        self.pt_demo_label = tk.Label(
            self.root, 
            text=pt_demo_str, 
            font=('Arial', 14),
            fg='#37afdb',justify='left')
        
        self.instruction = tk.Label(
            self.root, 
            text= 'Please describe why image(s) need(s) to be deleted *', 
            font=('Arial', 12))
        
        self.usr_justifctn_box = tk.Text(self.root, height=4)
        self.usr_justifctn_box.insert(1.0,'Enter a reason as to why the image(s) need(s) to be deleted')
        self.usr_justifctn_box.bind("<KeyRelease>", self.configure_submit_button)

        self.new_line = tk.Label(self.root, text= '\n', font=('Arial', 6))

        self.name_label = tk.Label(
            self.root, 
            text= 'Please provide your name to request deletion approval *', 
            font=('Arial', 12))
        
        self.name_txt_box = tk.Text(self.root, height=1, width= 50)
        if os.environ['USERNAME']==os.environ['COMPUTERNAME']:
            self.name_txt_box.insert(1.0, 'Name...')
        else:
            self.name_txt_box.insert(1.0, get_display_name())
        self.name_txt_box.bind("<KeyRelease>", self.configure_submit_button)
        
        self.required_label = tk.Label(
            self.root, 
            text="* = Required Fields", 
            font=('Arial', 12),
            fg='#EE4B2B',justify='left')

        self.submit_btn = tk.Button(
            self.root,
            text='Submit',
            command = self.submit,
            state = tk.DISABLED)
        
        self.click_btn= tk.PhotoImage(name='README', file='GitHub_Logo_small.png')

        self.github_msg = tk.Label(
            self.root, 
            text='README here:', 
            font=('Arial', 12),
            fg='#37afdb',
            justify='left')

        self.github_button= tk.Button(self.root, 
                               image=self.click_btn,
                               command= self.goto_git_hub, 
                               justify='left')

        
        # bind text boxes to delete on first click 
        self.usr_justifctn_box.bind('<Button-1>', self.on_click)
        if os.environ['USERNAME']==os.environ['COMPUTERNAME']:
            self.name_txt_box.bind('<Button-1>', self.on_click)

        # pack widgets to root window
        #self.debug.pack(padx=20, pady=20)
        self.label.pack(padx=20, pady=20)
        self.pt_demo_label.pack(padx=20, pady=20)
        self.instruction.pack()
        self.usr_justifctn_box.pack(padx=50, pady=10)
        self.new_line.pack()
        self.name_label.pack()
        self.name_txt_box.pack(pady=10)
        self.required_label.pack()
        self.submit_btn.pack(pady=20)
        self.github_msg.pack()
        self.github_button.pack()

        self.root.mainloop()
        

    # class functions
    def submit(self):

        # Parse INI
        config = configparser.ConfigParser()
        config.read('config.ini')
        url = config.get('URLs', 'FORMURL')

        # Get user input and inject into URL
        user_msg = self.usr_justifctn_box.get('1.0', tk.END)
        tech = self.name_txt_box.get('1.0', tk.END)
        params = {
            'entry.501677638': ipid, 
            'entry.349499540': pt_name, 
            'entry.800935706': mrn, 
            'entry.2083454847' : accession, 
            'entry.1340586078' : user_msg, 
            'entry.1963475195' : tech
            }

        # Replace 'chrome' with 'google-chrome' on Linux
        chrome_command = 'start chrome ' + '"' + url + urllib.parse.urlencode(params) + '"'
        
        subprocess.run(chrome_command, shell=True)
        messagebox.showinfo('Payload deployed!', 'Thank you for your request!')
        self.root.destroy()


    def on_click(self, event):
        event.widget.delete('1.0', tk.END) # clears string
        event.widget.unbind('<Button-1>')

    
    def goto_git_hub(self):
        webbrowser.open('https://github.com/MattyPACSiao/Deletion-Request')  




App()
'''
PURPOSE:
orchestrate sending relevant DICOM info to google form
1. take DICOM values from PACS
2. take deletion justification and tech name from GUI

TODO:

- Create final icon
- Make user entry fields mandatory

REF:
https://www.tcl.tk/man/tcl8.6/TkCmd/entry.html

GitHub repo:
https://github.com/MattyPACSiao/Deletion-Request
'''
