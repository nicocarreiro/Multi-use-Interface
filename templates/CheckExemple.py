import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function

# IntVar()
from tkinter import *


window = tk.Tk()

# Nome da janela
window.title("exemplo")

CheckVar1 = IntVar()
check = Checkbutton(window, text = "exemplo",variable = CheckVar1,onvalue = 1, offvalue=0).pack()
# check = Checkbutton(window, text = "Machine Learning",variable = CheckVar1,onvalue = 1, offvalue=0)
# check.pack()


# loop principal
window.mainloop()

print(CheckVar1.get())