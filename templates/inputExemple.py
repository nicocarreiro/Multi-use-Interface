import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function

def printinput():
    print(inputspace.get())


window = tk.Tk()

# Nome da janela
window.title("exemplo")


title = Label(window, text = "escreva")
title.grid(row=0)

inputspace = Entry(window)
inputspace.grid(row = 0, column = 1)


printtext = Button(window, command=printinput, text="print", width=24).grid(row=1, columnspan=2)

# loop principal
window.mainloop()
