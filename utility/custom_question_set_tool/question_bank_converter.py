import sys, subprocess
import glob, os, shutil

from tkinter import filedialog as fd

#Get
def getExcelFile ():
    print("Please select path to Excel file...")
    filename = fd.askopenfilename()
    return filename

#Execute PowerShell converter script
def convertExcelFile (filename):
    print("Converting " + filename + " to json format...")
    p = subprocess.run(["powershell.exe", ".\Convert-ExcelSheetToJson.ps1", filename],stdout=sys.stdout)

filename = getExcelFile()
print(filename)
convertExcelFile(filename)

#Copy question set to questionASets folder
files = glob.iglob(os.path.join(os.getcwd(), "*.json"))
for file in files:
    if os.path.isfile(file):
        shutil.copy2(file, "..\..\questionSets")

print("Done.")
