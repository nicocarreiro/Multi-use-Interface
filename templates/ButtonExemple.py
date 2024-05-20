import tkinter as tk
from tkinter import * #if you dont import this you need to put .tk before every function


window = tk.Tk()

# Nome da janela
window.title("exemplo")

# .pack() mostra o botao na janela
button_widget = Button(window,text="botao").pack()
# button_widget = Button(window,text="Welcome to DataCamp's Tutorial on Tkinter")
# button_widget.pack()


# loop principal
window.mainloop()