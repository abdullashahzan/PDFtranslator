import tkinter as tk
from tkinter.ttk import *
from PyPDF2 import PdfFileReader as pfr
from googletrans import Translator
from tkinter import filedialog as fd
import os
import threading

translator = Translator()

def openfilefolder():
    a = os.getcwd()
    os.startfile(rf'{a}')
    return

def select_file():
    global filename
    filetypes = (
        ('text files', '*.pdf'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Select PDF',
        initialdir='/',
        filetypes=filetypes)
    
    if filename != "":
        button1.config(state='normal',text="Translate", command=translatebtn)
        button2.config(text=filename)
    else:
        button1.config(state='disabled', command=translatebtn)
        button2.config(text='No file selected')
    return


def translatebtn():
    global filepath
    filepath = filename
    progress['value'] = 10
    root.update_idletasks()
    button1.config(state="disabled")
    button2.config(state='disabled')
    initialize(filepath)
    return

def initialize(filepath):
    label1.config(text="Reading file...")
    progress['value'] = 30
    root.update_idletasks()
    reader = pfr(rf'{filepath}')
    lt = []
    for i in range(reader.numPages):
        page = reader.pages[i]
        text = page.extractText()
        lt.append(text)
    t = threading.Thread(target= lambda : translation(lt))
    t.start()
    return

def translation(lst):
    try:
        label1.config(text= "Translating text, please wait...")
        progress['value'] = 70
        root.update_idletasks()
        ltr = []
        for i in lst:
            translatedtext = translator.translate(i, dest='en')
            ltr.append(translatedtext.text)
        label1.config(text= "Finishing...")
        listtotext = " ".join(ltr)
        a = listtotext.encode("ascii", "ignore")
        b = a.decode()
        finishing(b)
    except:
        label1.config(text="Error connecting to the internet :/")
    return

def finishing(text):
    label1.config(text="Finishing up...")
    progress['value'] = 90
    root.update_idletasks()
    nameoffile = os.path.basename(rf'{filepath}').split('/')[-1]
    nameoffile = nameoffile[:len(nameoffile)-4]
    
    with open(f"{nameoffile}TRANSLATED.txt", "w") as f:
        f.write(text)
    label1.config(text="Translation Successful")
    button1.config(text="Open file folder", command=openfilefolder, state='normal')
    button2.config(state='normal')
    progress['value'] = 100
    root.update_idletasks()
    label1.config(text="Translated successfully")
    return

root = tk.Tk()
root.geometry("310x300")
root.title("PDF Translator")

button2 = tk.Button(root, text="Select file", height=4, background='lightgreen', 
                    foreground='darkgreen', command=select_file)
button2.pack(fill=tk.X, pady=30, padx=10)

button1 = tk.Button(root, text="Translate", command=translatebtn, state="disabled",
                    width=30, height=2, background='violet', foreground="purple")
button1.pack(pady=20)

progress = Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')
progress.pack(pady=10, padx=15, fill=tk.X)

label1 = tk.Label(root, text="")
label1.pack(pady=5)

root.resizable(False,False)

root.mainloop()