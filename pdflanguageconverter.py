from PyPDF2 import PdfFileReader as pfr
from googletrans import Translator
import os

translator = Translator()

input1 = input("Please enter the path of the file that you want to convert: ")

filepath = rf"{input1}"
reader = pfr(filepath)

print("Starting reading file...")

lt = []
for i in range(reader.numPages):
    page = reader.pages[i]
    text = page.extractText()
    lt.append(text)

print("Finished reading, starting translation...")

ltr = []
for i in lt:
    translatedtext = translator.translate(i, dest='en')
    ltr.append(translatedtext.text)

print("Converting...")

listtotext = " ".join(ltr)

print("Cleaning text...")

a = listtotext.encode("ascii", "ignore")
b = a.decode()

print("Writing file...")

nameoffile = os.path.basename(filepath).split('/')[-1]
nameoffile = nameoffile[:len(nameoffile)-4]

with open(f"{nameoffile}TRANSLATED.txt", "w") as f:
    f.write(b)
    
print("Task executed successfully")



