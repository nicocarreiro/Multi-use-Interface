import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function

window = tk.Tk()

# Nome da janela
window.title("exemplo")

top_frame = Frame(window).pack()
bottom_frame = Frame(window).pack(side = "bottom")

btn1 = Button(top_frame, text = "Button1", fg = "red").pack() #'fg or foreground' is for coloring the contents (buttons)

btn2 = Button(top_frame, text = "Button2", fg = "green").pack()

btn3 = Button(bottom_frame, text = "Button3", fg = "purple").pack(side = "left") #'side' is used to left or right align the widgets

btn4 = Button(bottom_frame, text = "Button4", fg = "orange").pack(side = "left")


# loop principal
window.mainloop()