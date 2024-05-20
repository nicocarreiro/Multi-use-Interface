import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function



window = tk.Tk()

# Nome da janela
window.title("exemplo")

CheckVar1 = IntVar()
CheckVar2 = IntVar()
Checkbutton(window, text = "0/0",variable = CheckVar1,onvalue=1, offvalue=0).grid(row=0, column=0, sticky=W)
Checkbutton(window, text = "1/0", variable = CheckVar2, onvalue=1, offvalue=0).grid(row=1, column=0, sticky=W)

CheckVar3 = IntVar()
CheckVar4 = IntVar()
Checkbutton(window, text = "0/1",variable = CheckVar3,onvalue=1, offvalue=0).grid(row=0, column=1, sticky=W)
Checkbutton(window, text = "1/1", variable = CheckVar4, onvalue=1, offvalue=0).grid(row=1, column=1, sticky=W)

# loop principal
window.mainloop()

print(CheckVar1.get())