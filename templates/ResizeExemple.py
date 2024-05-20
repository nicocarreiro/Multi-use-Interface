import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function

window = tk.Tk()

window.geometry("900x600")

window.resizable(False, False)

Button(window, text="Button-1",height= 5, width=10).pack()
Button(window, text="Button-2",height=8, width=15).pack()
Button(window, text= "Button-3",height=10, width=30).pack()

window.mainloop()
