import tkinter as tk
from tkinter import *
 
window = tk.Tk()
 
# Adjust size 
window.geometry("500x500")
 
# configure first row size and binds it to the full length of left size of the window
Grid.rowconfigure(window,0,weight=1)

# configure second row size
Grid.rowconfigure(window,1,weight=2)

# configure third row size
Grid.rowconfigure(window,2,weight=2)

# binds the collumns to the full length of the window
Grid.columnconfigure(window,0,weight=1)
 
 
# Create Buttons
label = Label(window,text = "Text 1").grid(row=0,column=0,sticky="NSEW")
button_1 = Button(window,text="Button 1").grid(row=1,column=0,sticky="NSEW")
button_2 = Button(window,text="Button 2").grid(row=2,column=0,sticky="NSEW")
  
# Execute tkinter
window.mainloop()